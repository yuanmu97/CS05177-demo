def guess(scenes, faces, objects):
    """分析风险等级，每分析一张图片会被调用一次
    scenes: [{'name': 'a', 'score': 0.6}, ...]
    faces: [{'box_points': (0, 0, 100, 100)}, ...]
    objects: [{'name': 'a', 'box_points': (0, 0, 100, 100)}, ...]
    会修改所有 faces 和 objects，加上 'level' 属性，取值为 0～3 的整数
    """
    for i in faces:
        i['level'] = 3
    for i in objects:
        i['level'] = 1


def update(image):
    """更新模型，每张图片获得用户反馈后会被调用一次
    image: {
        'scenes': [{'name': 'a', 'score': 0.6}, ...],
        'rects': [{
            'type': self.type,
            'top': 0,
            'left': 0,
            'right': 100,
            'bottom': 100,
            'level': 1,  # 最初分析的等级
            'level_corrected': 3,  # 用户标定的等级，只会是 0 或 3
        }, ...],
    }
    """
    pass
