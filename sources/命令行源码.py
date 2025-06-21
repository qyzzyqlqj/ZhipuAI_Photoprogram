from zhipuai import ZhipuAI

your_api_keys = input('请填写您自己的APIKey:')
client = ZhipuAI(api_key=your_api_keys)
requirement = input("请输入绘图需求:")
model_name = input("填写需要调用的模型名称\n可选（请输入名字，不包括符号及括号）：\n1.cogview-4-250304(最新、付费)\n2.cogview-4（付费）\n3.cogview-3-flash（免费）\n请填写:")


print("请稍后,未响应属正常现象，不要过多点击防止卡死\n若两分钟之内未响应，请重试...")

response = client.images.generations(
    model=model_name, #填写需要调用的模型名称
    prompt=requirement)
print(response.data[0].url)


