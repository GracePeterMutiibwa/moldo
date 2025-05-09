# Generated from MoldoParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MoldoParser import MoldoParser
else:
    from MoldoParser import MoldoParser

# This class defines a complete listener for a parse tree produced by MoldoParser.
class MoldoParserListener(ParseTreeListener):

    # Enter a parse tree produced by MoldoParser#program.
    def enterProgram(self, ctx:MoldoParser.ProgramContext):
        pass

    # Exit a parse tree produced by MoldoParser#program.
    def exitProgram(self, ctx:MoldoParser.ProgramContext):
        pass


    # Enter a parse tree produced by MoldoParser#element.
    def enterElement(self, ctx:MoldoParser.ElementContext):
        pass

    # Exit a parse tree produced by MoldoParser#element.
    def exitElement(self, ctx:MoldoParser.ElementContext):
        pass


    # Enter a parse tree produced by MoldoParser#mblock_element.
    def enterMblock_element(self, ctx:MoldoParser.Mblock_elementContext):
        pass

    # Exit a parse tree produced by MoldoParser#mblock_element.
    def exitMblock_element(self, ctx:MoldoParser.Mblock_elementContext):
        pass


    # Enter a parse tree produced by MoldoParser#attribute.
    def enterAttribute(self, ctx:MoldoParser.AttributeContext):
        pass

    # Exit a parse tree produced by MoldoParser#attribute.
    def exitAttribute(self, ctx:MoldoParser.AttributeContext):
        pass


    # Enter a parse tree produced by MoldoParser#mblock_content.
    def enterMblock_content(self, ctx:MoldoParser.Mblock_contentContext):
        pass

    # Exit a parse tree produced by MoldoParser#mblock_content.
    def exitMblock_content(self, ctx:MoldoParser.Mblock_contentContext):
        pass


    # Enter a parse tree produced by MoldoParser#python_element.
    def enterPython_element(self, ctx:MoldoParser.Python_elementContext):
        pass

    # Exit a parse tree produced by MoldoParser#python_element.
    def exitPython_element(self, ctx:MoldoParser.Python_elementContext):
        pass


    # Enter a parse tree produced by MoldoParser#python_content_text.
    def enterPython_content_text(self, ctx:MoldoParser.Python_content_textContext):
        pass

    # Exit a parse tree produced by MoldoParser#python_content_text.
    def exitPython_content_text(self, ctx:MoldoParser.Python_content_textContext):
        pass


    # Enter a parse tree produced by MoldoParser#moldo_comment_element.
    def enterMoldo_comment_element(self, ctx:MoldoParser.Moldo_comment_elementContext):
        pass

    # Exit a parse tree produced by MoldoParser#moldo_comment_element.
    def exitMoldo_comment_element(self, ctx:MoldoParser.Moldo_comment_elementContext):
        pass


    # Enter a parse tree produced by MoldoParser#comment_content_inner.
    def enterComment_content_inner(self, ctx:MoldoParser.Comment_content_innerContext):
        pass

    # Exit a parse tree produced by MoldoParser#comment_content_inner.
    def exitComment_content_inner(self, ctx:MoldoParser.Comment_content_innerContext):
        pass



del MoldoParser