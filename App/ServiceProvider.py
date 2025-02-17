from dependency_injector import containers, providers

import View
import ViewModel
import Model

class ServiceProvider(containers.DeclarativeContainer):
    config = providers.Configuration()

    # model
    InspectionDataModel = providers.ThreadSafeSingleton(Model.InspectionDataModel)

    # view model
    MainWindowViewModel = providers.Factory(ViewModel.MainWindowViewModel)

    # view
    MainWindowView = providers.Factory(View.MainWindowView, viewModel=MainWindowViewModel)

        
