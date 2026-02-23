from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

prompt_template = PromptTemplate.from_template('单词:{word}, 反义词:{antonym}')
examples_data = [
    {"word": "上", "antonym": "下"},
    {"word": "大", "antonym": "小"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=prompt_template,
    examples=examples_data,
    prefix="给出给定单词的反义词",
    suffix="基于以上示例，{input_word}的反义词是？",
    input_variables=["input_word"]  # 前缀后缀中需要注入的变量名称
)

prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)
