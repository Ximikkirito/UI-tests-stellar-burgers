"""
react-dnd (HTML5Backend), который используется в конструкторе Stellar
Burgers, слушает нативные браузерные drag-события (dragstart/dragenter/
dragover/drop), а не мышиные события, которые эмулирует Selenium
ActionChains.drag_and_drop(). Поэтому перетаскивание в этом приложении
делается через явную JS-эмуляцию последовательности drag-событий с
общим DataTransfer — это стандартный обходной путь для react-dnd.
"""

_DRAG_AND_DROP_JS = """
const dataTransfer = new DataTransfer();
const source = arguments[0];
const target = arguments[1];

function fireEvent(element, type, dataTransfer) {
    const event = new Event(type, { bubbles: true, cancelable: true });
    event.dataTransfer = dataTransfer;
    element.dispatchEvent(event);
}

fireEvent(source, 'dragstart', dataTransfer);
fireEvent(target, 'dragenter', dataTransfer);
fireEvent(target, 'dragover', dataTransfer);
fireEvent(target, 'drop', dataTransfer);
fireEvent(source, 'dragend', dataTransfer);
"""


def drag_and_drop(driver, source_element, target_element):
    driver.execute_script(_DRAG_AND_DROP_JS, source_element, target_element)
