import requests
import cairosvg

# Function to save SVG content as a PNG image
def save_svg_as_png(svg_content, output_file_path):
    try:
        # Convert SVG content to PNG image using cairosvg
        cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_file_path)
        print("PNG image saved successfully:", output_file_path)
    except Exception as e:
        print("Error occurred while converting SVG to PNG:", e)

# Function to get SVG content from a URL
def get_svg_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch SVG content. Status code:", response.status_code)
    except Exception as e:
        print("Error occurred while fetching SVG content:", e)
    return None
import base64

def png_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        # 读取PNG图片的二进制数据
        image_binary = image_file.read()
        # 使用base64进行编码
        base64_encoded = base64.b64encode(image_binary).decode('utf-8')
        return base64_encoded

# # 用法示例
# file_path = "path/to/your/image.png"
# base64_data = png_to_base64(file_path)
# print(base64_data)

# Example usage:
if __name__ == "__main__":
    svg_url = "http://172.20.251.8:31788/views/login.html"  # Replace this with the actual URL of the SVG content
    png_file_path = "output.png"  # Replace this with the desired output file path

    svg_content = get_svg_content(svg_url)
    if svg_content:
        # save_svg_as_png(svg_content, png_file_path)
        print(svg_content)