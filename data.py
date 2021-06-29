from dataclasses import dataclass, field

from typing import List


@dataclass(frozen=True, order=True)
class PersonsDatabase:
    type: str
    database_name: str
    user_name: str
    password: str
    url: str
    port: int


@dataclass(frozen=True, order=True)
class VideosDatabase:
    type: str
    database_name: str
    user_name: str
    password: str
    url: str
    port: int


@dataclass(frozen=True, order=True)
class VideosStorage:
    id: int
    name: str
    owner: str
    path: str


@dataclass(frozen=True, order=True)
class DetectionsDatabase:
    type: str
    database_name: str
    user_name: str
    password: str
    url: str
    port: int


@dataclass(frozen=True, order=True)
class FaceEncodingsDatabase:
    type: str
    database_name: str
    user_name: str
    password: str
    url: str
    port: int


@dataclass(frozen=True, order=True)
class DetectionObject:
    id: int
    type: str


@dataclass(frozen=True, order=True)
class Person:
    id: int
    first_name: str
    last_name: str
    birthday: str


@dataclass(frozen=True, order=True)
class Video:
    id: int
    title: str
    owner: str
    description: str
    file_name: str
    source: str
    video_url: str
    downloaded: bool
    videoStorage_id: int
    path: str
    detected_persons: int
    length: int
    fps: int
    resolution: (int, int)
    size: float
    geo_coordinates: (float, float)
    recording_date: str
    upload_date: str
    quality: float
    tags: List[int] = field(default_factory=list)


@dataclass(frozen=True, order=True)
class Detections:
    id: int
    video_id: int
    frame_id: int
    detection_object: int
    object_id: int
    face_coordinates: (int, int)
    probability: float

"""

create table videos(
    id serial,
    title varchar(512),
    owner varchar(255),
    description varchar(5000),
    file_name varchar(255),
    source varchar(255),
    video_url varchar(1000),
    downloaded bool,
    videoStorage_id int,
    path varchar(1024),
    detected_persons int,
    length int,
    fps int,
    resolution_W int,
    resolution_H int,
    size float,
    geo_coordinates_W float,
    geo_coordinates_H float,
    recording_date varchar(50),
    upload_date varchar(50),
    quality float,
    tags varchar(2000)
);


create table detections(
    id serial,
    video_id int,
    frame_id int,
    detection_object int,
    object_id int,
    face_coordinates_W int,
    face_coordinates_H int,
    probability float
);


create table persons(
    id serial,
    first_name varchar(255),
    last_name varchar(255),
    birthday varchar(60)
);

create table face_encodings(
    id serial,
    person_id integer,
    photo_id integer,
    encoding float[4096]
);
create table photos(
    id serial,
    path varchar(1024)
)




"""