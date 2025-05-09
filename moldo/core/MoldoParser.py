# Generated from MoldoParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,74,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,5,0,20,8,0,10,0,12,0,23,9,0,1,0,1,0,1,1,1,
        1,1,1,3,1,30,8,1,1,2,1,2,5,2,34,8,2,10,2,12,2,37,9,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,3,1,3,1,4,1,4,5,4,49,8,4,10,4,12,4,52,9,4,1,5,1,5,
        1,5,3,5,57,8,5,1,5,1,5,1,6,1,6,1,7,1,7,3,7,65,8,7,1,7,1,7,1,8,4,
        8,70,8,8,11,8,12,8,71,1,8,0,0,9,0,2,4,6,8,10,12,14,16,0,0,73,0,21,
        1,0,0,0,2,29,1,0,0,0,4,31,1,0,0,0,6,42,1,0,0,0,8,50,1,0,0,0,10,53,
        1,0,0,0,12,60,1,0,0,0,14,62,1,0,0,0,16,69,1,0,0,0,18,20,3,2,1,0,
        19,18,1,0,0,0,20,23,1,0,0,0,21,19,1,0,0,0,21,22,1,0,0,0,22,24,1,
        0,0,0,23,21,1,0,0,0,24,25,5,0,0,1,25,1,1,0,0,0,26,30,3,4,2,0,27,
        30,3,10,5,0,28,30,3,14,7,0,29,26,1,0,0,0,29,27,1,0,0,0,29,28,1,0,
        0,0,30,3,1,0,0,0,31,35,5,1,0,0,32,34,3,6,3,0,33,32,1,0,0,0,34,37,
        1,0,0,0,35,33,1,0,0,0,35,36,1,0,0,0,36,38,1,0,0,0,37,35,1,0,0,0,
        38,39,5,11,0,0,39,40,3,8,4,0,40,41,5,4,0,0,41,5,1,0,0,0,42,43,5,
        8,0,0,43,44,5,9,0,0,44,45,5,10,0,0,45,7,1,0,0,0,46,49,3,2,1,0,47,
        49,5,6,0,0,48,46,1,0,0,0,48,47,1,0,0,0,49,52,1,0,0,0,50,48,1,0,0,
        0,50,51,1,0,0,0,51,9,1,0,0,0,52,50,1,0,0,0,53,54,5,2,0,0,54,56,5,
        11,0,0,55,57,3,12,6,0,56,55,1,0,0,0,56,57,1,0,0,0,57,58,1,0,0,0,
        58,59,5,5,0,0,59,11,1,0,0,0,60,61,5,6,0,0,61,13,1,0,0,0,62,64,5,
        3,0,0,63,65,3,16,8,0,64,63,1,0,0,0,64,65,1,0,0,0,65,66,1,0,0,0,66,
        67,5,14,0,0,67,15,1,0,0,0,68,70,5,13,0,0,69,68,1,0,0,0,70,71,1,0,
        0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,17,1,0,0,0,8,21,29,35,48,50,56,
        64,71
    ]

class MoldoParser ( Parser ):

    grammarFileName = "MoldoParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'<mblock'", "'<python'", "'<comment>'", 
                     "'</mblock>'", "'</python>'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'='", "<INVALID>", "'>'", "<INVALID>", 
                     "<INVALID>", "'</comment>'", "'<'" ]

    symbolicNames = [ "<INVALID>", "T_OPEN_MBLOCK", "T_OPEN_PYTHON", "T_OPEN_COMMENT", 
                      "T_CLOSE_MBLOCK", "T_CLOSE_PYTHON", "PCDATA", "WS", 
                      "T_ID", "T_EQUALS", "T_STRING", "T_END_OPEN_TAG", 
                      "MODE_WS_SKIP", "COMMENT_TEXT_CONTENT", "T_CLOSE_COMMENT", 
                      "COMMENT_LT_SIGN" ]

    RULE_program = 0
    RULE_element = 1
    RULE_mblock_element = 2
    RULE_attribute = 3
    RULE_mblock_content = 4
    RULE_python_element = 5
    RULE_python_content_text = 6
    RULE_moldo_comment_element = 7
    RULE_comment_content_inner = 8

    ruleNames =  [ "program", "element", "mblock_element", "attribute", 
                   "mblock_content", "python_element", "python_content_text", 
                   "moldo_comment_element", "comment_content_inner" ]

    EOF = Token.EOF
    T_OPEN_MBLOCK=1
    T_OPEN_PYTHON=2
    T_OPEN_COMMENT=3
    T_CLOSE_MBLOCK=4
    T_CLOSE_PYTHON=5
    PCDATA=6
    WS=7
    T_ID=8
    T_EQUALS=9
    T_STRING=10
    T_END_OPEN_TAG=11
    MODE_WS_SKIP=12
    COMMENT_TEXT_CONTENT=13
    T_CLOSE_COMMENT=14
    COMMENT_LT_SIGN=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MoldoParser.EOF, 0)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MoldoParser.ElementContext)
            else:
                return self.getTypedRuleContext(MoldoParser.ElementContext,i)


        def getRuleIndex(self):
            return MoldoParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = MoldoParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 14) != 0):
                self.state = 18
                self.element()
                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 24
            self.match(MoldoParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mblock_element(self):
            return self.getTypedRuleContext(MoldoParser.Mblock_elementContext,0)


        def python_element(self):
            return self.getTypedRuleContext(MoldoParser.Python_elementContext,0)


        def moldo_comment_element(self):
            return self.getTypedRuleContext(MoldoParser.Moldo_comment_elementContext,0)


        def getRuleIndex(self):
            return MoldoParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElement" ):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)




    def element(self):

        localctx = MoldoParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_element)
        try:
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 26
                self.mblock_element()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 27
                self.python_element()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 28
                self.moldo_comment_element()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mblock_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_OPEN_MBLOCK(self):
            return self.getToken(MoldoParser.T_OPEN_MBLOCK, 0)

        def T_END_OPEN_TAG(self):
            return self.getToken(MoldoParser.T_END_OPEN_TAG, 0)

        def mblock_content(self):
            return self.getTypedRuleContext(MoldoParser.Mblock_contentContext,0)


        def T_CLOSE_MBLOCK(self):
            return self.getToken(MoldoParser.T_CLOSE_MBLOCK, 0)

        def attribute(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MoldoParser.AttributeContext)
            else:
                return self.getTypedRuleContext(MoldoParser.AttributeContext,i)


        def getRuleIndex(self):
            return MoldoParser.RULE_mblock_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMblock_element" ):
                listener.enterMblock_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMblock_element" ):
                listener.exitMblock_element(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMblock_element" ):
                return visitor.visitMblock_element(self)
            else:
                return visitor.visitChildren(self)




    def mblock_element(self):

        localctx = MoldoParser.Mblock_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_mblock_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.match(MoldoParser.T_OPEN_MBLOCK)
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==8:
                self.state = 32
                self.attribute()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 38
            self.match(MoldoParser.T_END_OPEN_TAG)
            self.state = 39
            self.mblock_content()
            self.state = 40
            self.match(MoldoParser.T_CLOSE_MBLOCK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_ID(self):
            return self.getToken(MoldoParser.T_ID, 0)

        def T_EQUALS(self):
            return self.getToken(MoldoParser.T_EQUALS, 0)

        def T_STRING(self):
            return self.getToken(MoldoParser.T_STRING, 0)

        def getRuleIndex(self):
            return MoldoParser.RULE_attribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttribute" ):
                listener.enterAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttribute" ):
                listener.exitAttribute(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttribute" ):
                return visitor.visitAttribute(self)
            else:
                return visitor.visitChildren(self)




    def attribute(self):

        localctx = MoldoParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_attribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(MoldoParser.T_ID)
            self.state = 43
            self.match(MoldoParser.T_EQUALS)
            self.state = 44
            self.match(MoldoParser.T_STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Mblock_contentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MoldoParser.ElementContext)
            else:
                return self.getTypedRuleContext(MoldoParser.ElementContext,i)


        def PCDATA(self, i:int=None):
            if i is None:
                return self.getTokens(MoldoParser.PCDATA)
            else:
                return self.getToken(MoldoParser.PCDATA, i)

        def getRuleIndex(self):
            return MoldoParser.RULE_mblock_content

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMblock_content" ):
                listener.enterMblock_content(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMblock_content" ):
                listener.exitMblock_content(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMblock_content" ):
                return visitor.visitMblock_content(self)
            else:
                return visitor.visitChildren(self)




    def mblock_content(self):

        localctx = MoldoParser.Mblock_contentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_mblock_content)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 78) != 0):
                self.state = 48
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1, 2, 3]:
                    self.state = 46
                    self.element()
                    pass
                elif token in [6]:
                    self.state = 47
                    self.match(MoldoParser.PCDATA)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Python_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_OPEN_PYTHON(self):
            return self.getToken(MoldoParser.T_OPEN_PYTHON, 0)

        def T_END_OPEN_TAG(self):
            return self.getToken(MoldoParser.T_END_OPEN_TAG, 0)

        def T_CLOSE_PYTHON(self):
            return self.getToken(MoldoParser.T_CLOSE_PYTHON, 0)

        def python_content_text(self):
            return self.getTypedRuleContext(MoldoParser.Python_content_textContext,0)


        def getRuleIndex(self):
            return MoldoParser.RULE_python_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPython_element" ):
                listener.enterPython_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPython_element" ):
                listener.exitPython_element(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPython_element" ):
                return visitor.visitPython_element(self)
            else:
                return visitor.visitChildren(self)




    def python_element(self):

        localctx = MoldoParser.Python_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_python_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(MoldoParser.T_OPEN_PYTHON)
            self.state = 54
            self.match(MoldoParser.T_END_OPEN_TAG)
            self.state = 56
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 55
                self.python_content_text()


            self.state = 58
            self.match(MoldoParser.T_CLOSE_PYTHON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Python_content_textContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PCDATA(self):
            return self.getToken(MoldoParser.PCDATA, 0)

        def getRuleIndex(self):
            return MoldoParser.RULE_python_content_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPython_content_text" ):
                listener.enterPython_content_text(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPython_content_text" ):
                listener.exitPython_content_text(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPython_content_text" ):
                return visitor.visitPython_content_text(self)
            else:
                return visitor.visitChildren(self)




    def python_content_text(self):

        localctx = MoldoParser.Python_content_textContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_python_content_text)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(MoldoParser.PCDATA)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Moldo_comment_elementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_OPEN_COMMENT(self):
            return self.getToken(MoldoParser.T_OPEN_COMMENT, 0)

        def T_CLOSE_COMMENT(self):
            return self.getToken(MoldoParser.T_CLOSE_COMMENT, 0)

        def comment_content_inner(self):
            return self.getTypedRuleContext(MoldoParser.Comment_content_innerContext,0)


        def getRuleIndex(self):
            return MoldoParser.RULE_moldo_comment_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMoldo_comment_element" ):
                listener.enterMoldo_comment_element(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMoldo_comment_element" ):
                listener.exitMoldo_comment_element(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMoldo_comment_element" ):
                return visitor.visitMoldo_comment_element(self)
            else:
                return visitor.visitChildren(self)




    def moldo_comment_element(self):

        localctx = MoldoParser.Moldo_comment_elementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_moldo_comment_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(MoldoParser.T_OPEN_COMMENT)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 63
                self.comment_content_inner()


            self.state = 66
            self.match(MoldoParser.T_CLOSE_COMMENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Comment_content_innerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMENT_TEXT_CONTENT(self, i:int=None):
            if i is None:
                return self.getTokens(MoldoParser.COMMENT_TEXT_CONTENT)
            else:
                return self.getToken(MoldoParser.COMMENT_TEXT_CONTENT, i)

        def getRuleIndex(self):
            return MoldoParser.RULE_comment_content_inner

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment_content_inner" ):
                listener.enterComment_content_inner(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment_content_inner" ):
                listener.exitComment_content_inner(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComment_content_inner" ):
                return visitor.visitComment_content_inner(self)
            else:
                return visitor.visitChildren(self)




    def comment_content_inner(self):

        localctx = MoldoParser.Comment_content_innerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_comment_content_inner)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 68
                self.match(MoldoParser.COMMENT_TEXT_CONTENT)
                self.state = 71 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==13):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





