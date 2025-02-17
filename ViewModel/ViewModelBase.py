from PySide6.QtCore import QObject, Signal

import inspect

class ViewModelBase(QObject):
    PropertyChanged = Signal(str, object)

    def _onPropertyChanged(self, propertyName:str|None = None, value:object|None = None):
        if propertyName is None:
            propertyName = inspect.stack()[1].function
            value = getattr(self, propertyName, None)
            
        self.PropertyChanged.emit(propertyName, value)
