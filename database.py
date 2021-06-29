from data import PersonsDatabase, VideosDatabase, DetectionsDatabase, FaceEncodingsDatabase

videos_database = VideosDatabase(type='postgres', database_name='face_encodings', user_name='studioprojektowe', password='studioprojektowe1234',
                                   url='localhost', port=5432)
person_database = PersonsDatabase(type='postgres', database_name='face_encodings', user_name='studioprojektowe', password='studioprojektowe1234',
                                   url='localhost', port=5432)
detections_database = DetectionsDatabase(type='postgres', database_name='face_encodings', user_name='studioprojektowe', password='studioprojektowe1234',
                                   url='home.warloch.net', port=5432)
face_encodings_database = FaceEncodingsDatabase(type='postgres', database_name='face_encodings', user_name='studioprojektowe', password='studioprojektowe1234',
                                   url='localhost', port=5432)
photos_database = FaceEncodingsDatabase(type='postgres', database_name='face_encodings', user_name='studioprojektowe', password='studioprojektowe1234',
                                   url='localhost', port=5432)
