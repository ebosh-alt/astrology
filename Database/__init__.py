# from .accounts import Account, Accounts
# from .accounts_templates import AccountTemplate, AccountsTemplates
# from .customers import Customer, Customers
# from .managers import Manager, Managers
# from .projects import Project, Projects
# from .projects_work import ProjectWork, ProjectsWork
# from .responses_info import ResponseInfo, ResponsesInfo
# from .templates import Template, Templates
# from .workers import Worker, Workers

# accounts: Accounts = Accounts()
# customers: Customers = Customers()
# anagers: Managers = Managers()
# ccounts_templates: AccountsTemplates = AccountsTemplates()
# projects: Projects = Projects()
# projects_work: ProjectsWork = ProjectsWork()
# responses_info: ResponsesInfo = ResponsesInfo()
# templates: Templates = Templates()
# workers: Workers = Workers()

from .questionnaires import Questionnaire, Questionnaires

questionnaires: Questionnaires = Questionnaires()

__al__ = ("questionnaires", "Questionnaire")
