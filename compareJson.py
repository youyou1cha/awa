import json
from PIL import Image, ImageDraw, ImageFont

def generate_image_with_annotations(template_json, input_json):
    # 读取模板JSON数据
    template_data = json.loads(template_json)

    # 读取输入JSON数据
    input_data = json.loads(input_json)

    # 设置字体和字号
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 更改为适合您的字体路径
    font_size = 12
    # font = ImageFont.truetype(font_path, font_size)
    # font = ImageFont.truetype(font_size)

    # 设置图片尺寸和背景颜色
    image_width = 800
    image_height = 600
    background_color = (255, 255, 255)

    # 创建图片对象
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # 设置红色线条和标记的颜色
    line_color = (255, 0, 0)
    text_color = (255, 0, 0)

    # 遍历模板JSON的键值对
    for key, template_value in template_data.items():
        if template_value is not None:
            # 检查输入JSON中对应的键是否存在且值为空
            if key in input_data and input_data[key] is None:
                # 计算文本的宽度和高度
                # text_width, text_height = draw.textsize(key, font=font)
                text_width, text_height = draw.textsize(key)

                # 计算横线的起始和结束位置
                line_start = (10, text_height + 10)
                line_end = (text_width + 20, text_height + 10)

                # 绘制横线和文本
                draw.line([line_start, line_end], fill=line_color, width=2)
                # draw.text((25, 5), key, font=font, fill=text_color)
                draw.text((25, 5), key, fill=text_color)

    # 保存图片
    image.save("annotated_image.png")
    print("生成图片成功！")

# 示例模板JSON
template_json = """
{
  "name": "",
  "age": "",
  "email": "",
  "address": ""
}
"""

# 示例输入JSON
input_json = """
{
  "name": "John Doe",
  "age": null,
  "email": "johndoe@example.com",
  "address": null
}
"""

generate_image_with_annotations(template_json, input_json)
