import numpy as np
import cv2
from act_recog import predict_single_action
COLORS_10 = [(144, 238, 144), (178, 34, 34), (221, 160, 221), (0, 255,  0), (0, 128,  0), (210, 105, 30), (220, 20, 60),
             (192, 192, 192), (255, 228, 196), (50, 205, 50), (139,  0,
                                                               139), (100, 149, 237), (138, 43, 226), (238, 130, 238),
             (255,  0, 255), (0, 100,  0), (127, 255,  0), (255,  0,
                                                            255), (0,  0, 205), (255, 140,  0), (255, 239, 213),
             (199, 21, 133), (124, 252,  0), (147, 112, 219), (106, 90,
                                                               205), (176, 196, 222), (65, 105, 225), (173, 255, 47),
             (255, 20, 147), (219, 112, 147), (186, 85, 211), (199,
                                                               21, 133), (148,  0, 211), (255, 99, 71), (144, 238, 144),
             (255, 255,  0), (230, 230, 250), (0,  0, 255), (128, 128,
                                                             0), (189, 183, 107), (255, 255, 224), (128, 128, 128),
             (105, 105, 105), (64, 224, 208), (205, 133, 63), (0, 128,
                                                               128), (72, 209, 204), (139, 69, 19), (255, 245, 238),
             (250, 240, 230), (152, 251, 152), (0, 255, 255), (135,
                                                               206, 235), (0, 191, 255), (176, 224, 230), (0, 250, 154),
             (245, 255, 250), (240, 230, 140), (245, 222, 179), (0, 139,
                                                                 139), (143, 188, 143), (255,  0,  0), (240, 128, 128),
             (102, 205, 170), (60, 179, 113), (46, 139, 87), (165, 42,
                                                              42), (178, 34, 34), (175, 238, 238), (255, 248, 220),
             (218, 165, 32), (255, 250, 240), (253, 245, 230), (244, 164, 96), (210, 105, 30)]


# def draw_bbox(img, box, cls_name, identity=None, offset=(0,0)):
#     '''
#         draw box of an id
#     '''
#     x1,y1,x2,y2 = [int(i+offset[idx%2]) for idx,i in enumerate(box)]
#     # set color and label text
#     color = COLORS_10[identity%len(COLORS_10)] if identity is not None else COLORS_10[0]
#     label = '{} {}'.format(cls_name, identity)
#     # box text and bar
#     t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
#     cv2.rectangle(img,(x1, y1),(x2,y2),color,2)
#     cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
#     cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255], 1)
#     return img


def plot_one_box(x, ori_img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    img = ori_img
    tl = line_thickness or round(
        0.002 * max(img.shape[0:2])) + 1  # line thickness
    # color = color or [random.randint(0, 255) for _ in range(3)]
    color = (0, 203, 66)
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=1)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled
        cv2.putText(img,
                    label, (c1[0], c1[1] - 2),
                    0,
                    tl / 6, [225, 255, 255],
                    thickness=tf,
                    lineType=cv2.LINE_AA)
    return img

def draw_bboxes(ori_img, bbox, identities=None, offset=(0, 0)):
    img = ori_img
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        # id = int(identities[i]) if identities is not None else 0
        # color = COLORS_10[id % len(COLORS_10)]
        label = identities[i+1]
        # label = 'run'
        # t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        img = plot_one_box([x1, y1, x2, y2], img, (2,185,2), label)
        # cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        # cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        # cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    return img


    # ids_list = np.array([0])
    # objects_frame_list = np.array([[
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),
    #     np.zeros((64, 64, 3), dtype=int),]])
def frame_setting(ori_img, bbox, identities=None, offset=(0, 0)):
    img = ori_img
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        id = '{}{:d}'.format("", id)
        # xmin, ymin, xmax, ymax = bbox
        cropped_object = ori_img[y1:y2, x1:x2]

        resized_obj_img = cv2.resize(cropped_object, (64, 64))

        normalized_frame = resized_obj_img / 255
        if id not in ids_list:
            ids_list = np.append(ids_list, id)
            temp_arr = [np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        np.zeros((64, 64, 3), dtype=int),
                        ]
            objects_frame_list = np.append(
                objects_frame_list, [temp_arr], axis=0)
            id_index = np.where(ids_list == id)
        for i, j in enumerate(objects_frame_list[id_index][0]):
            if np.all(objects_frame_list[id_index][i] == 0, axis=None):
                print(i)
                objects_frame_list[id_index, i] = normalized_frame
                break

def act_pred(ori_img, bbox, identities=None, offset=(0, 0)):
    if np.any(objects_frame_list[i] == 0):
        action, confidence = predict_single_action(objects_frame_list[i])
    else:
        action = 'none'
        confidence = 0
    # print("action = ", action, "confidence = ", confidence)
    # print("ids_list", ids_list)
    # color = COLORS_10[id % len(COLORS_10)]
    img = plot_one_box([x1, y1, x2, y2], img, (144, 238, 144), action)
    return img


def softmax(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(x*5)
    return x_exp/x_exp.sum()


def softmin(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(-x)
    return x_exp/x_exp.sum()


if __name__ == '__main__':
    x = np.arange(10)/10.
    x = np.array([0.5, 0.5, 0.5, 0.6, 1.])
    y = softmax(x)
    z = softmin(x)
    import ipdb
    ipdb.set_trace()
