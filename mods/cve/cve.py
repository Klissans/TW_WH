import os
import shutil


from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.twui import *

def make_context_viewer_visible(xml):
    # Shows CV and tooltips in CV
    # language=javascript
    s = '''
        GetIf(
            this.GetProperty("cv_is_expanded") == 1,
            this.ChildList.Filter((c) =>
                {
                    GetIfElse(
                        Component("context_viewer").IsSearchActive,
                        (Component("context_viewer").IsInSearchResults(this) && Component("context_viewer").IsInSearchResults(c)) || Component("context_viewer").IsChildOfAnySearchResult(c),
                        true
                    )
                }
            )
        )
    '''
    set_context_callback(find_by_guid(xml, '653D2B8D-BDCB-4479-A25E53AB8A557445'), 'ContextList', s)


if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    rpfm = RPFM4Wrapper()
    
    edit_twui('ui/templates/context_viewer_entry',
              lambda xml: (
                  make_context_viewer_visible(xml)
              )
              )
    
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    MOD_NAME = '!Klissan_CVE'
    OUTPUT_DIR = 'output'
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)