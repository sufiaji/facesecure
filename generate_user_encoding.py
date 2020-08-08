import utils
import os
import cv2
import face_recognition

# # get existing userid
# select_statement = "select * from public." + utils.TABLE_USER 
# ok, engine = utils.getEngine()
# if ok==utils.OK_CODE:
#     sql = alchemy.text(select_statement)

# iterate image file inside folder
image_path = 'dataset4'
for (i, filename) in enumerate(os.listdir(image_path)):

    # extract information
    try:
        print("[INFO] processing image {}/{}".format(i + 1,	filename))
        user_id = filename.split('.')[0]
        full_filename = os.path.join(image_path, filename)
        image = cv2.imread(full_filename)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # face detection
        boxes = face_recognition.face_locations(rgb, model='cnn')
        # generate 128-encoding
        encoding = face_recognition.face_encodings(rgb, boxes)[0]
        
        # insert user
        utils.saveNewUser(user_id, user_id)

        # insert encodings
        okcode, dret = utils.saveNewEncoding(userId=user_id, encoding_array=encoding)
    except Exception as ex:
        pass
