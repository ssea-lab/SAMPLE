from .utils.getPara import Paras
from .utils import createFolders
from .generator.eoh import EOH
from .evaluator import run
from .management import pop_greedy
from .selection import prob_rank
from .problem import pre_deployment

paras = Paras()
problem = pre_deployment()
#deepseek
paras.set_paras(method = "eoh",
                problem = preblem,
                llm_api_endpoint = "api.deepseek.com",
                llm_api_key = "",#your api
                llm_model = "deepseek-chat",
                ec_pop_size = 4, # number of samples in each population
                ec_n_pop = 4,  # number of populations
                exp_n_proc = 4,  # multi-core parallel
                exp_debug_mode = False)

if __name__ == "__main__":
    createFolders.create_folders(paras.exp_output_path)
    select = prob_rank
    manage = pop_greedy
    eoh = EOH(paras, problem, select, manage)
    eoh.run()

