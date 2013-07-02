# -*- coding: utf-8 -*-
"""
   photolog.exif_reader
   ~~~~~~~~~~~~~~~~~~~~

    JPEG 사진에서 EXIF(교환 이미지 파일 형식, EXchangable Image File format)를 이용하여,
    PhotoLog에서 사용할 위치기반 정보를 얻어 온다.

    :copyright: (c) 2013 by 4mba
    :license: MIT LICENSE 2.0, see license for more details.
"""

# Library to extract Exif information from digital camera image files.
# https://github.com/ianare/exif-py
import EXIF;


class EXIFReader :

    file_path = "" 
    tags = ""
    def __init__(self, file_path) : 
        """ EXIFReader 클래스 생성자 """

        self.file_path = file_path 
        # Open image file for reading (binary mode)
        f = open(file_path, 'rb')
        
        # Return Exif tags
        self.tags = EXIF.process_file(f)        

        
    def get_thumbnails(self, file_path) :
        """EXIF 정에서 썸네일을 읽는 것이 가능할 경우 썸네일을 읽은 후 리턴한다. """

        print "ThumbNails"

    
    def get_geotag_lat(self):
        """EXIF 정보에서 GPS 정보를 읽어서 리턴한다.  """

        return self.tags["GPS GPSLatitude"]
    

    def get_geotag_lng(self):
        """EXIF 정보에서 GPS 정보를 읽어서 리턴한다.  """

        return self.tags["GPS GPSLatitude"]


    def print_all(self, file_path):
        """모든 EXIF 정보를 STDOUT에 출력한다.  """
        

        print "All Information of EXIF in " + file_path

        for tag in self.tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print "Key: %s, value %s" % (tag, self.tags[tag])


    
#All Information of EXIF in photos/2012-07-12 12.12.12.jpg
#================================================
#Key: GPS GPSLongitude, value [0, 843/100, 0]
#Key: GPS GPSLatitude, value [51, 3003/100, 0]
#Key: Image GPSInfo, value 594
#Key: GPS GPSLatitudeRef, value N
#Key: GPS GPSAltitudeRef, value 0
#Key: GPS GPSTimeStamp, value [11, 12, 1181/100]
#Key: GPS GPSAltitude, value 1820/317
#Key: GPS GPSLongitudeRef, value W

    







