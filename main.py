from typing import List, Optional, Tuple
from web import Wenjuan,Question,Submit
import random
from flet import (
    app,
    Row,
    Column,
    ListView,
    Ref,
    ControlEvent,
    TextField,
    Text,
    IconButton,
    ElevatedButton,
    Radio,
    RadioGroup,
    SnackBar,
    UserControl,
    Page
)


def clamp_number(num, a, b):
    return max(min(num, max(a,b)), min(a,b))

class FletQuestion(UserControl):
    def __init__(self, question, answers):
        super().__init__()
        self.question = question
        self.answers = answers
        self.choose = 0

    def build(self):
        return Column([
            Text(self.question),
            RadioGroup(
                Row(
                    [Radio(label=val, value=i) for (i, val) in enumerate(self.answers)]
                ),
                on_change=self.__radiogroup_onchange,
                value=0
            ),

        ])

    def __radiogroup_onchange(self, e: ControlEvent):
        self.choose = int(e.control.value)
        self.update()

    def choose_index(self) -> int:
        return self.choose


class FletQuestions(UserControl):
    def __init__(self, ref: Optional[Ref] = None):
        super().__init__(ref=ref)
        self.questions = ListView(auto_scroll=True,height=400, expand=1)
    def build(self):
        return self.questions

    def update_url(self, url):
        self.questions.controls.clear()
        (_questions, _) = self.page.webwjx.fetch_questions(url)
        for x in _questions:
            self.questions.controls.append(FletQuestion(x.get_question(), x.get_options()))
        self.update()

    def choose(self, index:int) -> int:
        return self.questions.controls[index].choose_index()

class FletCouter(UserControl):
    def __init__(self, name, value, ref: Optional[Ref] = None, range:Optional[Tuple[int, int]] = None):
        super().__init__(ref= ref)
        self.__value = str(value)
        self.__lable = name
        self.__text = Ref[Text]()
        self.__range = range
    def build(self):
        return Row(
                    [
                        Text(self.__lable),
                        IconButton('remove', on_click=self.minus_click),
                        Text(ref=self.__text, value=self.__value,text_align='right'),
                        IconButton('add', on_click=self.plus_click),
                    ],
                )

    def minus_click(self,e: ControlEvent):
        val = int(self.__text.current.value) - 1
        if self.__range is None:
            self.__text.current.value = str(val)
        else:
            (min, max) = self.__range
            self.__text.current.value = str(clamp_number(val, min, max))
        self.update()

    def plus_click(self, e: ControlEvent):
        val = int(self.__text.current.value) + 1
        if self.__range is None:
            self.__text.current.value = str(val)
        else:
            (min, max) = self.__range
            self.__text.current.value = str(clamp_number(val, min, max))
        self.update()

    def value(self):
        return int(self.__text.current.value)

url = Ref[TextField]()
submitcount = Ref[FletCouter]()
randomrange = Ref[FletCouter]()
precision = Ref[FletCouter]()
questions = Ref[FletQuestions]()

def submit_click(e: ControlEvent):
    _ct = submitcount.current.value()
    _rate = precision.current.value()
    _range = randomrange.current.value()
    e.page.show_snack_bar(SnackBar(Text('开始自动填写问卷'), open= True))
    e.page.update()
    for num in range(_ct):
        (_questions, _submit) = e.page.webwjx.fetch_questions(url.current.value)
        for (index, question) in enumerate(_questions):
            if question.get_options():
                i = questions.current.choose(index)
                if random.random() * 100 > _rate:
                    i = clamp_number(i + random.randint(-_range, _range), 0, len(question.get_options())-1)
                question.click(i)
        _submit.click()
        e.page.show_snack_bar(SnackBar(Text(f'已完成问卷{num + 1}次'), open= True))
        e.page.update()
    e.page.show_snack_bar(SnackBar(Text('完成啦'), open= True))
    e.page.update()



def url_submit(e: ControlEvent):
    e.page.show_snack_bar(SnackBar(Text('加载问卷星表单'), open= True))
    e.page.update()
    url = e.control.value
    questions.current.update_url(url)

def main(page: Page):
    def window_event(e: ControlEvent):
        if e.data == 'close':
            page.show_snack_bar(SnackBar(Text('正在关闭浏览器和程序，请稍等'), open= True))
            page.update()
            del page.webwjx
            page.window_destroy()
            
    page.title = '问卷星自动填写器 by shaoxi2010 (window edge)'
    page.window_height = 600
    page.window_width = 800
    page.window_resizable = False
    page.webwjx = Wenjuan()
    page.window_prevent_close = True
    page.on_window_event = window_event
    page.add(
        Row(
            [
                TextField(
                    ref = url,
                    hint_text='输入调查问卷表格地址',
                    autofocus= True,
                    on_submit=url_submit,
                    width=750,
                ),
            ],
            alignment="right",
            height=50
        ),
        Row(
            [
                FletCouter('准确率', 100, ref=precision, range=(0,100)),
                FletCouter('误差范围', 0, ref=randomrange, range=(0,100)),
                FletCouter('提交次数', 0, ref=submitcount, range=(0,100)),
                ElevatedButton('开始填表', width=200, on_click=submit_click)
            ],
            height=50,
        ),
        FletQuestions(ref=questions)
    )

if __name__ == "__main__":
    app(target=main)