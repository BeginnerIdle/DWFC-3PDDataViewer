from ViewModel.ViewModelBase import ViewModelBase

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QSizePolicy, QFileDialog
from PySide6.QtGui import QIntValidator, QMouseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView

from pathlib import Path

class MainWindowView(QMainWindow):
    BINDING_PROPERTY_FILENAME = "FileName"
    BINDING_PROPERTY_TRIGGER_OFFSET = "TriggerOffset"
    BINDING_PROPERTY_HTML_FILENAME = "HtmlFileName"

    def __init__(self, viewModel:ViewModelBase):
        super().__init__()

        self.__filePathLabel:QLabel = None
        self.__offsetLineEdit:QLineEdit = None
        self.__browser:QWebEngineView = None

        self.__viewModel = viewModel
        self.__viewModel.PropertyChanged.connect(self.__onViewModelPropertyChanged)

        self.setWindowTitle("Inspection Data Viewer")
        self.setGeometry(100, 100, 1000, 600)

        self.__buildUI()
    
#region UI build
    def __buildUI(self):
        # central
        mainWidget = QWidget()
        

        mainLayout = QVBoxLayout(mainWidget)
        self.setCentralWidget(mainWidget)

        mainLayout.addWidget(self.__buildControlPanel())
        mainLayout.addWidget(self.__buildDataPanel())

    def __buildControlPanel(self) -> QWidget:
        controlPanel = QWidget()
        controlPanel.setFixedHeight(32)
        controlPanel.setContentsMargins(2, 2, 2, 2)
        controlPanel.setStyleSheet("""
            QLabel {
                border: 1px solid gray;
                min-height: 28px;
                max-height: 28px;
            }
            QPushButton {
                border: 1px solid gray;
                min-width: 50px;
                max-width: 50px;
                min-height: 28px;
                max-height: 28px;
            }
            QLineEdit {
                border: 1px solid gray;
                min-width: 50px;
                max-width: 50px;
                min-height: 28px;
                max-height: 28px;
                qproperty-alignment: 'AlignRight';
            }                                   
        """)
        controlPanelLayout = QHBoxLayout(controlPanel)
        controlPanelLayout.setContentsMargins(0, 0, 0, 0)
        controlPanelLayout.setSpacing(2)

        # control panel - file path
        self.__filePathLabel = QLabel(self.__getViewModelProperty(self.BINDING_PROPERTY_FILENAME))
        self.__filePathLabel.mousePressEvent = self.__onFilePathLabelClicked
        controlPanelLayout.addWidget(self.__filePathLabel)
        # control panel - offset
        validator = QIntValidator()
        self.__offsetLineEdit = QLineEdit(str(self.__getViewModelProperty(self.BINDING_PROPERTY_TRIGGER_OFFSET)))
        self.__offsetLineEdit.editingFinished.connect(self.__onTriggerOffsetChanged)
        self.__offsetLineEdit.setValidator(validator)
        controlPanelLayout.addWidget(self.__offsetLineEdit)
        # control panel - run
        runButton = QPushButton("Run")
        controlPanelLayout.addWidget(runButton)

        return controlPanel

    def __buildDataPanel(self) -> QWidget:
        widget = QWidget()
        widget.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
        """)
        panel = QGridLayout(widget)

        panel.setColumnMinimumWidth(0, 100)
        panel.setColumnMinimumWidth(2, 100)
        panel.setColumnStretch(1, 1) # 가운데 열이 남은 공간을 채운다

        thmlFileName = Path(self.__getViewModelProperty(self.BINDING_PROPERTY_HTML_FILENAME)).absolute().as_uri()
        self.__browser = QWebEngineView()
        self.__browser.load(thmlFileName)
        self.__browser.setStyleSheet("""
            QWebEngineView {
                border: 1px solid gray;
            }
        """)
        panel.addWidget(self.__browser, 0, 0, 1, 3)

        decreaseButton = QPushButton()
        decreaseButton.clicked.connect(self.__onDecreaseButtonClicked)
        decreaseButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        panel.addWidget(decreaseButton, 0, 0)

        increaseButton = QPushButton()
        increaseButton.clicked.connect(self.__onIncreaseButtonClicked)
        increaseButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        panel.addWidget(increaseButton, 0, 2)

        return widget
#endregion

#region UI event action
    def __onIncreaseButtonClicked(self):
        offset = int(self.__offsetLineEdit.text()) + 1
        self.__setViewModelProperty(self.BINDING_PROPERTY_TRIGGER_OFFSET, offset)
    def __onDecreaseButtonClicked(self):
        offset = int(self.__offsetLineEdit.text()) - 1
        self.__setViewModelProperty(self.BINDING_PROPERTY_TRIGGER_OFFSET, offset)
    
    def __onFilePathLabelClicked(self, event:QMouseEvent):
        filePath, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "CSV (*.csv)")
        if filePath:
            self.__setViewModelProperty(self.BINDING_PROPERTY_FILENAME, filePath)

    def __onTriggerOffsetChanged(self):
        offset = int(self.__offsetLineEdit.text())
        self.__setViewModelProperty(self.BINDING_PROPERTY_TRIGGER_OFFSET, offset)
#endregion

#region MVVM Helper
    def __onViewModelPropertyChanged(self, propertyName:str, value:object):
        if propertyName == self.BINDING_PROPERTY_FILENAME:
            self.__filePathLabel.setText(value)
        elif propertyName == self.BINDING_PROPERTY_TRIGGER_OFFSET:
            self.__offsetLineEdit.setText(str(value))
        elif propertyName == self.BINDING_PROPERTY_HTML_FILENAME:
            self.__browser.reload()
            print("reload success")
        else:
            print(f"not support property {propertyName}")
    
    def __getViewModelProperty(self, propertyName:str) -> object|None:
        return getattr(self.__viewModel, propertyName, None)
    
    def __setViewModelProperty(self, propertyName:str, value:object):
        try:
            setattr(self.__viewModel, propertyName, value)
        except:
            print(f"Failed to set property {propertyName} to {value}")
#endregion



