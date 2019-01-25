from menu import Menu, MenuItem
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

Menu.add_item("home", MenuItem(_('mainmenu:home'),
                               reverse('main:home'),
                               exact_url=True,
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:leader_experiments'),
                               reverse('leader:experiments'),
                               check=lambda x: x.user.is_authenticated and
                                               x.user.is_leader()
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:leader_profile'),
                               reverse('leader:profile'),
                               check=lambda x: x.user.is_authenticated and
                                               x.user.is_leader()
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:mailinglist'),
                               '#',
                               check=lambda x: not x.user.is_authenticated
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:register'),
                               '#',
                               check=lambda x: not x.user.is_authenticated
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:change_password'),
                               '#',
                               check=lambda x: x.user.is_authenticated
                               ))

Menu.add_item("footer", MenuItem(_('main:globals:login'),
                                 reverse('main:login'),
                                 check=lambda x: not x.user.is_authenticated
                                 ))

Menu.add_item("footer", MenuItem(_('main:globals:logout'),
                                 reverse('main:logout'),
                                 check=lambda x: x.user.is_authenticated
                                 ))
