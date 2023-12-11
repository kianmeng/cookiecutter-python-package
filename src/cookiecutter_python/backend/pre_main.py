import typing as t
from .helpers import supported_interpreters
from .hosting_services import Engine
from .gen_docs_common import get_docs_gen_internal_config


def pre_main(request):
    """Do preparatory steps Generation process, by settings things as the Template Context.

    Args:
        **kwargs: Arbitrary keyword arguments.
    """
    ## External Services Clients Initialization ## 
    # clients "how to question" 3rd party web services like pypi, and rtd
    # making http request to web servers hosting endpoints for APIs
    request.check = Engine.create(request.config_file, request.default_config)

    # initialize the check_results
    request.check_results = request.check.check(request.web_servers)

    # Case 1: NON Interactive Mode <--> `request.no_input == True`
    #   - if interpreters is None, then no user config file supplied in CLI
    # Case 2: Interactive Mode <--> `request.no_input == False`
    #   - always meaningful value, since Interactive Dialog ensures that
    interpreters: t.Optional[t.Mapping[str, t.Sequence[str]]] = supported_interpreters(request.config_file, request.no_input)
    # if None, then we are in NON interactive mode, but no User Config, passed in CLI

    if interpreters:  # update cookiecutter extra_context
        # supported interpreters supplied either from yaml or from user's input
        request.extra_context = dict(
            request.extra_context or {},
            **{
                'interpreters': interpreters,
            }
        )

    # define the 'docs' folder path to use, per docs builder
    # request.extra_context = dict(
    #     request.extra_context or {},
    #     **{
    #         'docs': {
    #             # TODO: unit-test compatibility of below with post_gen_project
    #             # test that 'find_docs_folder' functions correctly
    #             # make sure tests will break in case of future diviation
    #             # aka make the case a regression test 
    #             'mkdocs': 'docs-mkdocs',
    #             'sphinx': 'docs-sphinx',
    #         },
    #     }
    # )
    return request
