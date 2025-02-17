from ViewModel.ViewModelBase import ViewModelBase

from PySide6.QtCore import Signal
import pandas as pd
import tempfile
import plotly.express as px

class MainWindowViewModel(ViewModelBase):
    PlotDataUpdated = Signal(pd.DataFrame)

    def __init__(self):
        super().__init__()

        self.__fileName:str = ""
        self.__triggerOffset:int = 0
        self.__htmlFileName = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name

        from App.Application import Application
        self.__inspectionDataModel = Application.instance().service().InspectionDataModel()
        self.__inspectionDataModel.PlotDataUpdated.connect(self.__onInspectionDataModelPlotDataUpdated)
        self.__inspectionDataModel.updateFromFile(self.__fileName, self.__triggerOffset)

#region property for Binding to Model
    @property
    def FileName(self) -> str:
        return self.__fileName
    @FileName.setter
    def FileName(self, value:str):
        if self.__fileName != value:
            self.__fileName = value
            self.__inspectionDataModel.updateFromFile(self.__fileName, self.__triggerOffset)
            self._onPropertyChanged()
    
    @property
    def TriggerOffset(self) -> int:
        return self.__triggerOffset
    @TriggerOffset.setter
    def TriggerOffset(self, value:int):
        if self.__triggerOffset != value:
            self.__triggerOffset = value
            self.__inspectionDataModel.chageTriggerOffset(self.__triggerOffset)
            self._onPropertyChanged()
    
    @property
    def HtmlFileName(self) -> str:
        return self.__htmlFileName
    @HtmlFileName.setter
    def HtmlFileName(self, value:str):
        if self.__htmlFileName != value:
            self.__htmlFileName = value
            self._onPropertyChanged()
#endregion

#region event callback
    def __onInspectionDataModelPlotDataUpdated(self, plotData:pd.DataFrame):
        fig = px.box(plotData, x="Category", y="BED", points='all', hover_data=['Trigger'])
        fig.update_layout(title="BED Distribution", xaxis_title="Category", yaxis_title="BED")
        print("update success")
        fig.write_html(self.__htmlFileName)
        print("write success")
        self._onPropertyChanged("HtmlFileName", self.__htmlFileName)
#endregion


