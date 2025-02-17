from PySide6.QtCore import QObject, Signal

from dataclasses import dataclass
from threading import Lock
import csv
import pandas as pd

@dataclass
class InspectionData:
    Trigger:int
    FED:float
    BED:float
    Vision:int

class InspectionDataModel(QObject):
    PlotDataUpdated = Signal(pd.DataFrame)

    COLUMN_NAME_TRIGGER = "Trigger"
    COLUMN_NAME_FED = "FED"
    COLUMN_NAME_BED = "BED"
    COLUMN_NAME_VISION = "Vision"
    COLUMN_NAME_CATEGORY = "Category"

    def __init__(self):
        super().__init__()
        
        self.__rawData:list[InspectionData] = list()
        self.__plotData:pd.DataFrame = pd.DataFrame(
            columns=[
                self.COLUMN_NAME_TRIGGER,
                self.COLUMN_NAME_FED,
                self.COLUMN_NAME_BED,
                self.COLUMN_NAME_VISION,
                self.COLUMN_NAME_CATEGORY
            ]
        )

        self.__fileName:str = ""
        self.__triggerOffset:int = 0
        self.__dataLock:Lock = Lock()
    
    def chageTriggerOffset(self, offset:int):
        with self.__dataLock:
            self.__triggerOffset = offset
            if not self.__updatePlotData():
                self.__resetPlotData()
            
            self.PlotDataUpdated.emit(self.__plotData)
    
    def updateFromFile(self, fileName:str, offset:int|None = None):
        with self.__dataLock:
            self.__fileName = fileName
            if offset is not None: self.__triggerOffset = offset

            if not self.__updateRawData() or not self.__updatePlotData():
                self.__resetRawData()
                self.__resetPlotData()
            
            self.PlotDataUpdated.emit(self.__plotData)

    def getPlotData(self) -> pd.DataFrame:
        with self.__dataLock:
            return self.__plotData

    def __updateRawData(self) -> bool:
        try:
            with open(self.__fileName, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                try:
                    next(reader) # 1행 무시 (header)

                    rawData = [
                        InspectionData(int(row[0]), float(row[4]), float(row[5]), int(row[6]))
                        for row in reader if len(row) > 6
                    ]
                    self.__rawData = rawData
                except:
                    return False
            return True
        except:
            print(f"Failed to load file {self.__fileName}")
            return False

    def __updatePlotData(self) -> bool:
        try:
            plotData = pd.DataFrame([data.__dict__ for data in self.__rawData])
            plotData[self.COLUMN_NAME_BED] = plotData[self.COLUMN_NAME_BED].shift(- self.__triggerOffset)
            plotData[self.COLUMN_NAME_CATEGORY] = plotData[self.COLUMN_NAME_VISION].apply(lambda x: "Normal" if x == 0 else "Plasma")
            plotData.dropna()

            self.__plotData = plotData
            return True
        except:
            return False
    
    def __resetPlotData(self):
        plotData = pd.DataFrame(
            columns=[
                self.COLUMN_NAME_TRIGGER,
                self.COLUMN_NAME_FED,
                self.COLUMN_NAME_BED,
                self.COLUMN_NAME_VISION,
                self.COLUMN_NAME_CATEGORY
            ]
        )
        self.__plotData = plotData
    
    def __resetRawData(self):
        self.__rawData = list()


        
        
