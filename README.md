# fsm_ant
Simplest FSM ant AI

Простая реализация поведения муравья, который должен подобрать листик и вернуться в муравейник.

Мозг муравья представлен классом FSM(finite state machine),
который реализует два метода:
* метод set_state() - задает текущее состояние
* метод update() - проверяет если ли состояние и запускает его

Идеи для доработки.
* Продвинутый алгоритм движения для муравья - например расчет кратчайшего расстояния до листа в обход мышки
* Расчет расстояние не до координат курсора а до ближайшего к нему краю сферы, которая рисуется вокруг координат курсора.
* Добавление вывода информации на статус бар - текущее состояние муравья, расстояние до листа и тд

### Запуск
```python
pip install -r requirements.py
python ant_game.py
```
