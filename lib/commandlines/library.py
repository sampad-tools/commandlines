#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class Command(object):
    def __init__(self):
        self.argv = sys.argv[1:]  # removes executable from CL argument list
        self.arguments = Arguments(self.argv)  # create a positional arguments object
        self.switches = Switches(self.argv)    # create a list of command line switches
        self.defs = Definitions(self.argv)     # create a command line definition dictionary
        self.argc = len(self.argv)  # length of the argument list
        self.arg0 = self.arguments._get_argument(0)  # define the first positional argument
        self.arg1 = self.arguments._get_argument(1)  # define the second positional argument
        self.arg2 = self.arguments._get_argument(2)  # define the third postitional argument
        self.arg3 = self.arguments._get_argument(3)  # define the fourth positional argument
        self.arg4 = self.arguments._get_argument(4)  # define the fifth positional argument
        self.arglp = self.arguments._get_argument(self.argc - 1)  # define the last positional argument
        self.subcmd = self.arg0
        self.subsubcmd = self.arg1
        self.firstarg = self.arg0
        self.secondarg = self.arg1
        self.thirdarg = self.arg2
        self.fourtharg = self.arg3
        self.fiftharg = self.arg4
        self.has_args = (len(self.arguments) > 0)  # test for presence of at least one argument (boolean)

    # ------------------------------------------------------------------------------------------
    # [ get_next_positional method ] (string)
    #  Return the NEXT positional argument to a command line argument
    #    arg_recipient = the positional argument (at list index n) to test for next positional argument
    #    returns next positional argument string at list index n + 1 or empty string if no next positional
    # ------------------------------------------------------------------------------------------
    def get_next_positional(self, arg_recipient):
        recipient_position = self.arguments._get_arg_position(arg_recipient)
        return self.arguments._get_arg_next(recipient_position)

    # ------------------------------------------------------------------------------------------
    # [ validates method ] (boolean)
    #    Test that there is at least one argument in the command string
    #    returns boolean for presence of one or more arguments to the executable
    # ------------------------------------------------------------------------------------------
    def validates(self):
        return self.argc > 0

    def validates_n(self, number):
        return self.argc == number

    def includes_switches(self):
        return len(self.switches) > 0

    def includes_definitions(self):
        return len(self.defs) > 0

    def contains_switch(self, switch_test_string):
        if switch_test_string in self.switches:
            return True
        else:
            return False

    def contains_definition(self, def_test_string):
        if def_test_string in self.defs.keys():
            return True
        else:
            return False

    def get_definition(self, def_name_string):
        if def_name_string in self.defs.keys():
            return self.defs[def_name_string]
        else:
            return ""


    # ------------------------------------------------------------------------------
    # [flag_arg method] (string)
    #   Return the argument string assigned to a flag
    # ------------------------------------------------------------------------------
    def flag_arg(self, flag_string):
        for match_string in self.optobj:
            if match_string.startswith(flag_string) and '=' in match_string:
                flag_list = match_string.split("=") #split the flag on the equal symbol = list with [option, argument]
                return flag_list[1] #return the argument to the flag option
            else:
                pass
        return ""  # return an empty string if unable to parse the argument

    # ------------------------------------------------------------------------------------------
    # [ option method ] (boolean)
    #   Test that the command includes an option (option_string parameter)
    #    option_string = the option string to test for in the command
    #    arugment_required = boolean - is an argument to this option required (default = no)?
    #    returns boolean for presence of the cmd_str
    # ------------------------------------------------------------------------------------------
    def option(self, option_string, argument_required = False):
        if option_string in self.optobj:
            argument_to_option = self.arguments._get_arg_next(self.arguments._get_arg_position(option_string))
            if argument_required and (argument_to_option == "" or argument_to_option.startswith("-")):
                return False
            else:
                return True
        else:
            return False

    # ------------------------------------------------------------------------------
    # [ option_arg method ] (string)
    #  Return the argument string to an option
    # ------------------------------------------------------------------------------
    def option_arg(self, option_string):
        return self.arguments._get_arg_next(self.arguments._get_arg_position(option_string))

    # ------------------------------------------------------------------------------------------
    # [ option_with_arg method ] (boolean)
    # Test that the command includes an option (option_string parameter) and argument to that option
    #    option_string = the option string to test for in the command
    #    arugment_required = boolean - is an argument to this option required (default = yes)?
    #    returns boolean for presence of the option_string AND the argument
    # ------------------------------------------------------------------------------------------
    #  test that command includes an option (option_string parameter) that includes an argument (=option(option_string, True))

    def option_with_arg(self, option_string, argument_required = True):
        if option_string in self.optobj:
            argument_to_option = self.arguments._get_arg_next(self.arguments._get_arg_position(option_string))
            if argument_required and (argument_to_option == "" or argument_to_option.startswith("-")):
                return False # argument is either missing or is another option, return false
            else:
                return True
        else:
            return False  # option is not present

    # ------------------------------------------------------------------------------
    # [ option_exists method ] (boolean)
    #  Test whether there are any options in the command string
    #  returns boolean value for test "Is there at least one option?"
    # ------------------------------------------------------------------------------
    def option_exists(self):
        if len(self.optobj) > 0:
            return True
        else:
            return False
    # ------------------------------------------------------------------------------
    #  Provides the following commands for all applications that use the framework:
    #  -- help
    #  -- usage
    #  -- version
    #  These methods are accessed from the app.py module, main() as method calls on the command line object
    #  Parsing logic is coded below
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Help Command/Switches Handler
    # ------------------------------------------------------------------------------
    def help(self):
        if self.option("--help") or self.option("-h"):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------
    # Usage Command/Switches Handler
    # ------------------------------------------------------------------------------
    def usage(self):
        if self.option("--usage"):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------
    # Version Command/Switches Handler
    # ------------------------------------------------------------------------------
    def version(self):
        if self.option("--version")  or self.option("-v"):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------
    # print the arguments with their corresponding argv list position to std out
    # ------------------------------------------------------------------------------
    def show_args(self):
        x = 0
        for arg in self.argv:
            print("argv[" + str(x) + "] = " + arg)
            x += 1


# ------------------------------------------------------------------------------
# [ Arguments Class ]
#   All command line arguments
#   Object type: Python list (inherited)
#
# ------------------------------------------------------------------------------


class Arguments(list):
    def __init__(self, argv):
        self.argv = argv
        list.__init__(self, self.argv)

    #  return argument at position specified by the 'position' parameter
    def _get_argument(self, position):
        if self.argv and len(self.argv) > position:
            return self.argv[position]
        else:
            return ""

    # return position of user specified argument in the argument list
    def _get_arg_position(self, test_arg):
        if self.argv:
            if test_arg in self.argv:
                return self.argv.index(test_arg)
            else:
                return -1

    # return the argument at the next position following a user specified positional argument
    def _get_arg_next(self, position):
        if len(self.argv) > (position + 1):
            return self.argv[position + 1]
        else:
            return ""


# ------------------------------------------------------------------------------
# [ Switches Class ]
#   Command line switches
#   Object type: Python list (inherited)
#   Syntax included:  -s or --long
# ------------------------------------------------------------------------------


class Switches(list):
    def __init__(self, argv):
        self.argv = argv
        list.__init__(self, self._make_switch_list())

    # make a list of the options in the command (defined as anything that starts with "-" character)
    def _make_switch_list(self):
        switchargv = []
        for x in self.argv:
            if x.startswith("-") and "=" not in x:
                x.replace("-", "")  # remove the '-' character(s from the switch before adding to list
                switchargv.append(x)

        return switchargv


# ---------------------------------------------------------------------------------------------
# [ Definitions Class ]
#   Command line options with definition syntax
#   Object type: Python dictionary (inherited)
#   Syntax included: -x <positional def>   --something <positional def>  --something=definition
#   Mapping: {option1: definition1, option2: definition2, ... optionX: definitionX}
# ---------------------------------------------------------------------------------------------


class Definitions(dict):
    def __init__(self, argv):
        self.argv = argv
        dict.__init__(self, self._make_definitions_obj())

    def _make_definitions_obj(self):
        defmap = {}
        arglist_length = len(self.argv)
        counter = 0
        for x in self.argv:
            # defines -option=definition syntax
            if x.startswith("-") and "=" in x:
                split_def = x.split("=")
                defmap[split_def[0]] = split_def[1]
            # defines -d <positional def> or --define <positional def> syntax
            elif x.startswith("-") and counter < arglist_length:
                if not self.argv[counter + 1].startswith("-"):
                    defmap[x] = self.argv[counter + 1]

            counter += 1

        return defmap
