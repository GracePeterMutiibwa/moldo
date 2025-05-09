# Generated from MoldoParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MoldoParser import MoldoParser
else:
    from MoldoParser import MoldoParser

# This class defines a complete generic visitor for a parse tree produced by MoldoParser.

class MoldoParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MoldoParser#program.
    def visitProgram(self, ctx:MoldoParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#element.
    def visitElement(self, ctx:MoldoParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#mblock_element.
    def visitMblock_element(self, ctx:MoldoParser.Mblock_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#attribute.
    def visitAttribute(self, ctx:MoldoParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#mblock_content.
    def visitMblock_content(self, ctx:MoldoParser.Mblock_contentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#python_element.
    def visitPython_element(self, ctx:MoldoParser.Python_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#python_content_text.
    def visitPython_content_text(self, ctx:MoldoParser.Python_content_textContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#moldo_comment_element.
    def visitMoldo_comment_element(self, ctx:MoldoParser.Moldo_comment_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#comment_content_inner.
    def visitComment_content_inner(self, ctx:MoldoParser.Comment_content_innerContext):
        return self.visitChildren(ctx)



del MoldoParser