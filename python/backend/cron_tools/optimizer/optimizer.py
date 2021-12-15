""""
========================== Microgrid Modeling and Simulation Software (MERGE - E72) =========================
"""
import os, sys
from cron_tools.optimizer.tools.input_data_processing import InputData
from cron_tools.optimizer.tools.mathematical_model_construction import MathematicalModel
from cron_tools.optimizer.tools.summary_results_construction import SummaryResults


def optimizer_milp_function(input_data):

    if not input_data:
        return None
    else:

        data = InputData(input_data)

        # Calculating necessaries parameters for the model construction
        data.CalculateParameters()

        """"
        ========================== Constructing Mathematical Modelling =========================
        """
        print("\n************* START: Formulating mathematical model - Cold Start  *************\n", flush=True)

        model = MathematicalModel(data)

        # Creating necessary list for the model construction
        model.ConstructionOfLists()

        # Formulating the problem
        prob_CS = model.ProblemFormultion_ColdStart()

        # Writing the problem in a file .lp
        # model.WritingProblemFileCS(prob_CS,"Cold_Start")

        print("\n************* END: Formulating mathematical model - Cold Start  *************\n", flush=True)

        ######################################################################
        #================ SOLVING MATHEMATICAL MODEL ====================
        ######################################################################

        print("\n************* START: Solving mathematical model - Cold Start *************\n", flush=True)

        # Giving attributes of object model to new object results
        results = model

        # Solving the mathematical model via PULP - Cold Start
        results.Solving_Model_CS(prob_CS)

        print("\n************* END: Solving mathematical model - Cold Start *************\n")

        data.SavingApproximations(results)


        # Calculating necessaries parameters for the model construction
        data.CalculateParameters()

        """"
        ========================== Constructing Mathematical Modelling =========================
        """

        model_PL = MathematicalModel(data)

        # Creating necessary list for the model construction
        model_PL.ConstructionOfLists()

        print("\n************* START: Formulating mathematical model - PL  *************\n", flush=True)

        # Formulating the problem
        prob = model_PL.ProblemFormulation()


        # Writing the problem in a file .lp
        # model_PL.WritingProblemFile(prob,"EMS_three_phase_for_Microgrids")

        print("\n************* END: Formulating mathematical model - PL  *************\n", flush=True)

        ######################################################################
        #================ SOLVING MATHEMATICAL MODEL ====================
        ######################################################################

        print("\n************* START: Solving mathematical model - PL *************\n", flush=True)

        # Giving attributes of object model to new object results
        results = model_PL

        # Solving the mathematical model via PULP - Cold Start
        results.Solving_Model(prob)

        print("\n************* END: Solving mathematical model - PL *************\n")

        ######################################################################
        #========================= SUMMARY RESULTS  ==========================
        ######################################################################

        # Criando um objeto da classe SummaryResults

        summary_results = SummaryResults(data, results)

        print("\n************* START: Summary Results  *************\n")

        if results.Status == "Optimal":
            output = summary_results.WritingFeasibleOutputFile()
            print("\n************* END: Summary Results  *************\n")
            print("Solution written to output_file.json")

        else:
            output = summary_results.WritingUnfeasibleOutputFile()
            print("\n************* END: Summary Results  *************\n")
            print("Default solution written to output_file.json")

        ######################################################################
        #========================= RETURNING SOLUTION  =======================
        ######################################################################

        return output