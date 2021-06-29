import json
import os
import time

import cv2
import psycopg2
from psycopg2 import Error
from deepface import DeepFace
import face_recognition
import youtube_dl
import numpy as np
import pandas as pd
from database import person_database, face_encodings_database, photos_database, videos_database

IMAGE_DATABASE_PATH = os.path.abspath('../test001')


class ChildFinder:
    included_extensions = ['jpg', 'jpeg', 'bmp', 'png']

    def __init__(self, person_database, face_encodings_database, photos_database, video_database, model_name='DeepFace',
                 detector_backend='opencv'):
        self.person_database = person_database
        self.video_database = video_database
        self.face_encodings_database = face_encodings_database
        self.photos_database = photos_database
        self.model = DeepFace.build_model(model_name)
        self.detector_backend = detector_backend
        self.downloader = Downloader(self.video_database)
        self.distance_metric = "euclidean_l2"
        self.ui = None

    @staticmethod
    def find_cosine_distance(source_representation, test_representation):
        a = np.matmul(np.transpose(source_representation), test_representation)
        b = np.sum(np.multiply(source_representation, source_representation))
        c = np.sum(np.multiply(test_representation, test_representation))
        return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

    @staticmethod
    def connect_to_db(database):
        try:
            conn = psycopg2.connect(host=database.url,
                                    dbname=database.database_name,
                                    user=database.user_name,
                                    password=database.password,
                                    port=database.port)
            return conn
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    @staticmethod
    def l2_normalize(x):
        return x / np.sqrt(np.sum(np.multiply(x, x)))

    @staticmethod
    def find_euclidean_distance(source_representation, test_representation):
        if type(source_representation) == list:
            source_representation = np.array(source_representation)

        if type(test_representation) == list:
            test_representation = np.array(test_representation)

        euclidean_distance = source_representation - test_representation
        euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
        euclidean_distance = np.sqrt(euclidean_distance)
        return euclidean_distance

    @staticmethod
    def find_threshold(model_name, distance_metric):

        base_threshold = {'cosine': 0.40, 'euclidean': 0.55, 'euclidean_l2': 0.75}

        thresholds = {
            'VGG-Face': {'cosine': 0.40, 'euclidean': 0.55, 'euclidean_l2': 0.75},
            'OpenFace': {'cosine': 0.10, 'euclidean': 0.55, 'euclidean_l2': 0.55},
            'Facenet': {'cosine': 0.40, 'euclidean': 10, 'euclidean_l2': 0.80},
            'DeepFace': {'cosine': 0.23, 'euclidean': 64, 'euclidean_l2': 0.64},
            'DeepID': {'cosine': 0.015, 'euclidean': 45, 'euclidean_l2': 0.17},
            'Dlib': {'cosine': 0.07, 'euclidean': 0.6, 'euclidean_l2': 0.6},
            'ArcFace': {'cosine': 0.6871912959056619, 'euclidean': 4.1591468986978075,
                        'euclidean_l2': 1.1315718048269017}
        }

        threshold = thresholds.get(model_name, base_threshold).get(distance_metric, 0.4)

        return threshold

    def download_videos_from_urls_file(self, ui, filename, download=True):
        self.downloader.load_urls_from_file(filename)
        self.downloader.download(ui=ui, download=download)

    def get_photos_ids_from_path(self, paths):
        connection = self.connect_to_db(self.photos_database)
        cursor = connection.cursor()
        query = "SELECT id FROM photos WHERE path in(%s)"
        person_ids = None
        try:
            cursor.execute(query, paths)
            connection.commit()
            person_ids = cursor.fetchall()[0]
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return person_ids

    @staticmethod
    def strip_person_name_from_path(path):
        return path.split('/')[-2]
    @staticmethod
    def strip_person_name_from_path2(path):
        return path.split('/')[-1]

    def add_face_encodings_to_database(self, photo_paths, face_encodings, persons_ids, photos_path):
        if len(face_encodings) == len(persons_ids) == len(photos_path):
            connection = self.connect_to_db(self.face_encodings_database)
            cursor = connection.cursor()

            queryEncodings = "SELECT encoding FROM face_encodings WHERE person_id = " + str(persons_ids[0])

            query = "INSERT INTO face_encodings (person_id, encoding, photo_path) VALUES(%s, %s, %s) RETURNING id"

            try:
                cursor.execute(queryEncodings)
                encodingsInBase = [list(map(float, encodingInBase[0])) for encodingInBase in cursor.fetchall()]
                connection.commit()
                if encodingsInBase != face_encodings:
                    for encoding in encodingsInBase:
                        if encoding in face_encodings:
                            face_encodings.remove(encoding)
                            print("removed encoding from list")
                    data = [detection for detection in
                            zip([persons_ids[0]] * len(face_encodings), face_encodings, photo_paths)]
                    cursor.executemany(query, data)
                    connection.commit()
                else:
                    print("add encodings has been skipped")
            except (Exception, Error) as error:
                print("Error while connecting to PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
        else:
            print('len(face_encodings) /= len(persons_ids) /= len(photo_ids)')

    def encode_person_folder(self, ui, person_folder_path: str, add_to_database=False) -> (list, list, list):
        self.ui = ui
        faces_encodings = []
        person_images = [fn for fn in os.listdir(f'{person_folder_path}') if
                         any(fn.endswith(ext) for ext in self.included_extensions)]
        person_id = None
        connection = self.connect_to_db(self.person_database)
        cursor = connection.cursor()
        first_name = ''.join(person_folder_path.split('/')[-1].split(' ')[0])
        last_name = ''.join(person_folder_path.split('/')[-1].split(' ')[1:])

        query = "SELECT id FROM person WHERE first_name=%s AND last_name=%s"

        try:
            cursor.execute(query, (first_name, last_name))
            new_person = True if cursor.rowcount == 0 else False

            if new_person:
                query2 = "INSERT INTO person (first_name, last_name, birth_date) VALUES(%s, %s, %s) RETURNING id"

                cursor.execute(query2, (first_name, last_name, 'brak_info'))
            person_id = cursor.fetchone()[0]
            print(person_id)
            connection.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        try:
            connection = self.connect_to_db(self.photos_database)
            cursor = connection.cursor()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        for p, image in enumerate(person_images):
            self.ui.handle_Progress1(block_num=p, total_size=len(person_images) - 1)
            faces_encodings.append(
                DeepFace.represent(f'{person_folder_path}/{image}', model=self.model, enforce_detection=False,
                                   detector_backend=self.detector_backend, align=True))

        if add_to_database:
            self.add_face_encodings_to_database(photos_path=[i for i in range(len(faces_encodings))],
                                                face_encodings=faces_encodings,
                                                photo_paths=[f'{person_folder_path}/{photo_path}' for photo_path in
                                                             person_images],
                                                persons_ids=[person_id for _ in range(len(faces_encodings))])
        return [f'{person_folder_path}/{image}' for image in person_images], faces_encodings, [person_id for _ in
                                                                                               range(
                                                                                                   len(faces_encodings))]

    def get_representations_from_database(self):
        result = []
        query = "SELECT fe.photo_path, fe.person_id, fe.encoding from face_encodings fe"
        try:
            connection = self.connect_to_db(self.face_encodings_database)
            cursor = connection.cursor()
            cursor.execute(query)
            result = [[row[0], row[1], list(map(float, row[2]))] for row in cursor.fetchall()]
            connection.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

        return result

    def recognize_person_representation(self, target_encoding):
        data = self.get_representations_from_database()
        resp_objects = []
        i = 0
        for photo_path, person_id, source_encoding in data:
            self.ui.handle_Progress2(block_num=i, total_size=len(data)-1)
            i = i + 1
            if self.distance_metric == 'cosine':
                distance = self.find_cosine_distance(target_encoding, source_encoding)
            elif self.distance_metric == 'euclidean':
                distance = self.find_euclidean_distance(target_encoding, source_encoding)
            elif self.distance_metric == 'euclidean_l2':
                distance = self.find_euclidean_distance(self.l2_normalize(target_encoding),
                                                        self.l2_normalize(source_encoding))
            resp_obj = {
                "verified": True if distance <= self.find_threshold('DeepFace', self.distance_metric) else False
                , "distance": distance
                , "photo_path": photo_path
                , "max_threshold_to_verify": self.find_threshold('DeepFace', self.distance_metric)
                , "similarity_metric": "euclidean_l2"
                , "person_id": person_id
            }
            resp_objects.append(resp_obj)
        df = pd.DataFrame(resp_objects, columns=["verified", "distance", "photo_path", "max_threshold_to_verify",
                                                 "similarity_metric"])
        df['identity'] = df['photo_path'].apply(self.strip_person_name_from_path)
        return df

    def recognize_person_from_photo(self, ui, img_path):
        self.ui = ui
        target_encoding = DeepFace.represent(img_path, model=self.model, enforce_detection=False,
                                             detector_backend=self.detector_backend, align=True)
        df = self.recognize_person_representation(target_encoding=target_encoding)
        return df[df['verified'].eq(True)]


class Downloader:
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    @staticmethod
    def connect_to_db(database):
        try:
            conn = psycopg2.connect(host=database.url,
                                    dbname=database.database_name,
                                    user=database.user_name,
                                    password=database.password,
                                    port=database.port)
            return conn
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def __init__(self, videos_database, download_path=None, ydl_opts=None, urls=None):
        self.videos_database = videos_database
        self.download_path = download_path if download_path else os.path.abspath(
            '/'.join(os.getcwd().split('/')[:-1]) + '/resources/downloaded')
        self.ydl_opts = ydl_opts if ydl_opts else {
            'format': 'best',
            'outtmpl': self.download_path + '/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
            'ignoreerrors': 'True',
            'logger': self.MyLogger(),
            'progress_hooks': [self.my_hook],
        }
        self.urls = urls if urls else []
        self.ui = None

    def my_hook(self, d):
        if d['status'] == 'finished':
            self.ui.handle_download_output(
                f'{d["filename"]}')
                # f'{d["filename"]} | speed:{d["speed"] if d["speed"] else 0} Bps | elapsed: {d["elapsed"]} s | size: {d["downloaded_bytes"]} B')

    def load_urls_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.urls = [x.replace('\n', '') for x in file.readlines()]

    def download(self, ui, download=True):
        self.ui = ui
        query = "INSERT INTO videos (file_path, info) VALUES (%s, %s)"
        file_paths = []
        jsons_data = []
        for url in self.urls:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=download)
                if info_dict:
                    if info_dict.get('entries'):
                        for entry in info_dict.get('entries'):
                            jsons_data.append(json.dumps(entry))
                            file_paths.append(
                                self.download_path + f'/{entry.get("playlist")}/{entry.get("playlist_index")} - {entry.get("title")}.{entry.get("ext")}')
        try:
            connection = self.connect_to_db(database=videos_database)
            cursor = connection.cursor()
            params = [(path, json) for path, json in zip(file_paths, jsons_data)]
            cursor.executemany(query, params)
            connection.commit()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()


def main():
    child_finder = ChildFinder(person_database=person_database, face_encodings_database=face_encodings_database,
                               photos_database=photos_database, video_database=videos_database)
    child_finder.download_videos_from_urls_file('../resources/links1.txt', download=False)

    child_finder.recognize_person_from_photo(os.path.abspath("../test001/Ada Harrington/0.jpg"))


if __name__ == '__main__':
    main()
