import json
import csv

def compare_json(templatejson, comparejson, output_csv):
    # 读取JSON数据
    datatemplate = json.loads(templatejson)
    datacampare = json.loads(comparejson)

    # 获取所有键的集合
    all_keys = set(datatemplate.keys()).union(set(datacampare.keys()))

    # 创建CSV文件并写入标题行
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['allkey', '采控', '对比'])

        # 比较两个JSON的值并写入CSV文件
        for key in all_keys:
            value1 = datatemplate.get(key)
            value2 = datacampare.get(key)

            # if value1 != value2:
            writer.writerow([key, value1, value2])

    print("CSV文件生成成功！")

# 示例JSON数据
templatejson = '''
{
  "name": "John Doe",
  "age": 30,
  "email": "johndoe@example.com",
  "address": "123 Main St"
}
'''

comparejson = '''
{
  "name": "John Smith",
  "age": 30,
  "email": "johnsmith@example.com",
  "phone": "+1234567890"
}
'''

# 指定输出的CSV文件路径
output_csv = "comparison_result.csv"

# 比较JSON并写入CSV
compare_json(templatejson, comparejson, output_csv)
