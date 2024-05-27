ASSERT_DIR = 'assets/'
WUGUANZHU_JSON_DIR = ASSERT_DIR + 'json/wuguanzhu'
XUEWANG_JSON_DIR = ASSERT_DIR + 'json/xuewang'

WINDOW_TITLE = '"慧眼卫视"——AI驱动的眼底图像智能处理软件'

# Texts:
APP_NAME = '慧眼卫视'
COMPANY_NAME = '第一人民医院 Inc.'
COMPANY_URL = 'https://www.xzsdyyy.com/'
APP_DESCRIPTION = '慧眼卫视“——AI驱动的眼底图像智能处理软件'

BASIC_INFO_TEXT = '''慧眼卫视基于深度学习和智能优化算法等先进技术，有针对性地改进了医学影像信息系统中存在的缺点和不足之处。集成了医学图像处理、图像可视化、病灶自动定位等功能，
实现了医学图像自动识别、自动标注、自动定位全过程。
    - 限1人使用
    - 可以在多台设备通过账号登陆同时使用
    - 适用于PC
    - 适用于windows7以上操作系统
    - 1TB(1.000 GB)安全云存储空间
    - 使用Docker技术进行模块化和容器化部署云服务后台
    - 针对图像数据和分析数据进行高级安全存储
    - 包括无灌注区域识别工具、糖网分级工具和血网分割工具
    - 直观简洁，且易于使用，任何人都可以轻松操作''' 

WUGUANZHU_TOOL_BUTTON_INFOS = [
    ('加载图片', ASSERT_DIR + 'icons/加载图片.png'),
    ('读取历史', ASSERT_DIR + 'icons/读取历史.png'),
    ('大图识别', ASSERT_DIR + 'icons/大图识别.png'),
    ('矩形增加', ASSERT_DIR + 'icons/矩形增加.png'),
    ('矩形删除', ASSERT_DIR + 'icons/矩形删除.png'),
    ('手动添加', ASSERT_DIR + 'icons/手动添加.png'),
    ('手动删除', ASSERT_DIR + 'icons/手动删除.png'),
    ('区域生长', ASSERT_DIR + 'icons/区域生长.png'),
    ('眼底分区', ASSERT_DIR + 'icons/眼底分区.png'),
    ('矩形占比', ASSERT_DIR + 'icons/矩形占比.png'),
    ('撤销操作', ASSERT_DIR + 'icons/撤销操作.png'),
    ('数据保存', ASSERT_DIR + 'icons/数据保存.png'),
    ('掩膜保存', ASSERT_DIR + 'icons/掩模保存.png'),
]

TOOL_BUTTON_NUM = len(WUGUANZHU_TOOL_BUTTON_INFOS)

XUEWANG_TOOL_BUTTON_INFOS = [
    ('加载图片', ASSERT_DIR + 'icons/加载图片.png'),
    ('读取历史', ASSERT_DIR + 'icons/读取历史.png'),
    ('血网分割', ASSERT_DIR + 'icons/大图识别.png'),
    # ('矩形增加', ASSERT_DIR + 'icons/矩形增加.png'),
    # ('矩形删除', ASSERT_DIR + 'icons/矩形删除.png'),
    # ('手动添加', ASSERT_DIR + 'icons/手动添加.png'),
    # ('手动删除', ASSERT_DIR + 'icons/手动删除.png'),
    # ('区域生长', ASSERT_DIR + 'icons/区域生长.png'),
    # ('撤销操作', ASSERT_DIR + 'icons/撤销操作.png'),
    ('数据保存', ASSERT_DIR + 'icons/数据保存.png'),
    # ('掩膜保存', ASSERT_DIR + 'icons/掩模保存.png'),
]

XUEWANG_BUTTON_NUM = len(XUEWANG_TOOL_BUTTON_INFOS)

TOOL_BUTTON_FONT_NAME = 'SimHei'
TOOL_BUTTON_FONT_SIZE = 12

ADD_ICON_PATH = ASSERT_DIR + 'icons/add.png'


WUGUANZHU_IMAGE_PATHS = [
    ASSERT_DIR + 'images/wuguanzhu/demo_1.jpg',
    ASSERT_DIR + 'images/wuguanzhu/demo_2.jpg',
    ASSERT_DIR + 'images/wuguanzhu/demo_3.jpg',
    ASSERT_DIR + 'images/wuguanzhu/demo_4.jpg',
    ASSERT_DIR + 'images/wuguanzhu/demo_5.jpg',
]

DEMO_IMAGE_PATHS = WUGUANZHU_IMAGE_PATHS

XUEWANG_IMAGE_PATHS = [
    ASSERT_DIR + 'images/xuewang/Image_01L.jpg',
    ASSERT_DIR + 'images/xuewang/Image_01R.jpg',
    ASSERT_DIR + 'images/xuewang/Image_02L.jpg',
    ASSERT_DIR + 'images/xuewang/Image_02R.jpg',
    ASSERT_DIR + 'images/xuewang/Image_03L.jpg',
]

XUEWANG_TARGET_IMAGE_PATHS = [
    ASSERT_DIR + 'images/xuewang_target/Image_01L_1stHO.png',
    ASSERT_DIR + 'images/xuewang_target/Image_01R_1stHO.png',
    ASSERT_DIR + 'images/xuewang_target/Image_02L_1stHO.png',
    ASSERT_DIR + 'images/xuewang_target/Image_02R_1stHO.png',
    ASSERT_DIR + 'images/xuewang_target/Image_03L_1stHO.png',
]

# Paths:
WINDOW_ICON_PATH = 'assets/icons/window_icon.svg'
SPLASH_SCREEN_PATH = 'assets/images/paper.png'

SMALL_MODEL_PATH = ASSERT_DIR + 'models/logs3/best_epoch_weights.pth'
LARGE_MODEL_PATH = ASSERT_DIR + 'models/logs4/best_epoch_weights.pth'

XUEWANG_MODEL_PATH = ASSERT_DIR + 'models/xuewang/best_epoch_weights.pth'