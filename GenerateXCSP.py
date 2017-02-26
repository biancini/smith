from lxml import etreefrom XCSPNodeAgents     import XCSPNodeAgentsfrom XCSPNodeVariables  import XCSPNodeVariablesfrom XCSPNodeDomains    import  XCSPNodeDomainsfrom XCSPNodePredicates import XCSPNodePredicatesfrom XCSPNodeConstraint import XCSPNodeConstraintfrom XCSPNodeFunctions  import XCSPNodeFunctionsfrom WashingMachine import WashingMachinefrom Boiler         import Boilerfrom SolarPanel     import SolarPanelfrom ConstraintWeightedSum  import ConstraintWeightedSumfrom ConstraintCostFunction import ConstraintCostFunction##################### PARAMETERS #####################time_steps = 18max_power_available = 30cost = [1] * time_stepstau = [1] * time_stepsinstance = etree.Element("instance") # Root Nodepresentation = etree.Element(   "presentation",                                name = "SMIThSampleProblem",                                maxConstraintArity = str(time_steps),                                maximize = "false",                                format = "XCSP 2.1_FRODO")# agents      = etree.Element("agents", nbAgents = '0')# domains     = etree.Element("domains", nbDomains = '0')# variables   = etree.Element("variables", nbVariables = '0')# predicates  = etree.Element("predicates", nbPredicates = '0')# constraints = etree.Element("constraints", nbConstraints = '0')## instance.append( presentation )# instance.append( agents )# instance.append( domains )# instance.append( variables )# instance.append( predicates )# instance.append( constraints )domains   = XCSPNodeDomains()variables = XCSPNodeVariables( domains )functions   = XCSPNodeFunctions()predicates  = XCSPNodePredicates()constraints = XCSPNodeConstraint( predicates, functions )agents    = XCSPNodeAgents( variables, constraints )wm = WashingMachine("WashingMachine", time_steps)wm.endsBefore(28)boiler_initial_qty = 80boiler = Boiler("Boiler", time_steps, boiler_initial_qty)boiler.endsBefore(23)solar_panel = SolarPanel("SolarPanel", time_steps)agents.addAgent( wm )agents.addAgent( boiler )agents.addAgent( solar_panel )### Genero i constraint globali# Constraint sulla massima potenza consumatafor t in range(0, time_steps):    variabili = [ a.variables[t] for a in agents.elements ]    c = ConstraintWeightedSum("max_power_constraint_t_{}".format(t), agents.elements, variabili, "le", max_power_available)    constraints.addConstraint( c )# Constraint di non poter consumare piu' di quanto disponibilefor t in range(0, time_steps):    variabili = [ a.variables[t] for a in agents.elements ]    c = ConstraintWeightedSum("inject_power_is_no_more_than_consumed_power_t_{}".format(t), agents.elements, variabili, "ge", 0)    constraints.addConstraint( c )# Genero la funzione di costofor t in range(0, time_steps):    variabili = [a.variables[t] for a in agents.elements]    c = ConstraintCostFunction("cost_function_t_{}".format(t), agents.elements, variabili, cost[t], tau[t])    constraints.addConstraint(c)instance.append( presentation )instance.append( agents.node() )instance.append( domains.node() )instance.append( variables.node() )instance.append( predicates.node() )instance.append( constraints.node() )instance.append( functions.node() )content = etree.tostring(instance, encoding='UTF-8', method="xml", pretty_print = True)content = content.replace(b"&lt;", b"<").replace(b"&gt;", b">")with open("smith.xcsp", 'wb') as out:    out.write(content)