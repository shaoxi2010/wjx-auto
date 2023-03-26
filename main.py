from web import Wenjuan
from flet import (
    app,
    Row,
    Ref,
    ControlEvent,
    TextField,
    Text,
    IconButton,
    ElevatedButton,
    SnackBar,
    Page
)

url = Ref[TextField]()
count = Ref[Text]()

def submit_click(e: ControlEvent):
    ct = int(count.current.value)
    if ct < 0:
        ct = 0
    e.page.show_snack_bar(SnackBar(Text('有点慢，等等浏览器响应'), open=True))
    e.page.update()
    wjx = Wenjuan()
    for _ in range(ct):
        wjx.answer_question(url.current.value)
    e.page.show_snack_bar(SnackBar(Text('完成啦'), open= True))
    e.page.update()

def minus_click(e: ControlEvent):
    count.current.value = str(int(count.current.value) - 1)
    e.page.update()


def plus_click(e: ControlEvent):
    count.current.value = str(int(count.current.value) + 1)
    e.page.update()



def main(page: Page):
    page.title = '问卷星自动填写器'
    page.window_resizable = False
    page.window_height = 200
    page.add(
        TextField(
            ref = url,
            hint_text='输入调查问卷表格地址',
            autofocus= True,
        ),
        Row(
            [
                Text('总提交次数：'),
                IconButton('remove', on_click=minus_click),
                Text(ref=count, value=0,text_align='right', width=100),
                IconButton('add', on_click=plus_click),
                ElevatedButton('开始填表', width=200, on_click=submit_click)
            ],
            alignment='center',
        )
    )
app(target=main)