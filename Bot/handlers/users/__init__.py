from .menu import menu_rt
from .payment import payment_rt
from .packets import packets_rt
from .mailing import mailing_rt
from .support import support_rt
from .filling_profile import filling_profile_rtfrom .ask_question import question_rt
from .rectification import rectification_rt

users_routers = (menu_rt, support_rt, packets_rt, mailing_rt, filling_profile_rt, question_rt, rectification_rt)
