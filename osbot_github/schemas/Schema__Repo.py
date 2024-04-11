from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Schema__Repo(Kwargs_To_Self):
    name         : str
    owner        : str
    full_name    : str
    description  : str
    url          : str
    pushed_date  : int
    created_date : int
    updated_date : int
    size         : int
    stars        : int
    forks        : int
    watchers     : int
    language     : str
    topics       : str