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

    file_path = None 
    tags = None
    
    def __init__(self, file_path) : 
        """ EXIFReader 클래스 생성자 """

        self.file_path = file_path 
        # Open image file for reading (binary mode)
        f = open(file_path, 'rb')
        
        # Return Exif tags
        self.tags = EXIF.process_file(f)        


    
    def get_geotag_lat(self):
        """EXIF 정보에서 GPS 정보를 읽어서 리턴한다.  """
        result = None
        
        try: 
            result = self.tags["GPS GPSLatitude"]
        except KeyError, e:
            result = "43, 4641/100, 0"
            print "EXIF KeyError : No GPS GPSLatitude, Use default value. %s" % str(e)


        return result
    

    def get_geotag_lng(self):
        """EXIF 정보에서 GPS 정보를 읽어서 리턴한다.  """
        result = None
        
        try: 
            result = self.tags["GPS GPSLongitude"]
        except KeyError, e: 
            result = "11, 1533/100, 0"
            print "EXIF KeyError : No GPS GPSLongitude, Use default value. %s" % str(e)

        return result


    def get_taken_time(self):
        """EXIF 정보에서 사진을 찍은 시간을 리턴한다  """

        return self.tags["Image DateTime"]


    def print_all(self):
        """모든 EXIF 정보를 STDOUT에 출력한다.  """
        

        print "All Information of EXIF in " + self.file_path

        for tag in self.tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print "Key: %s, value %s" % (tag, self.tags[tag])



