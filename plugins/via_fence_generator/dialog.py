# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class Dialog
###########################################################################

class Dialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Via Fence Generator"), pos = wx.DefaultPosition, size = wx.Size( 900,500 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        subSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Reference plane settings") ), wx.VERTICAL )

        subsubSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
        subsubSizer1.SetFlexibleDirection( wx.BOTH )
        subsubSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( subSizer1.GetStaticBox(), wx.ID_ANY, _(u"Net:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        subsubSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        lstViaNetChoices = []
        self.lstViaNet = wx.Choice( subSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstViaNetChoices, 0 )
        self.lstViaNet.SetSelection( 0 )
        subsubSizer1.Add( self.lstViaNet, 0, wx.ALL, 5 )

        self.chkUpdateViaNet = wx.CheckBox( subSizer1.GetStaticBox(), wx.ID_ANY, _(u"Automatically update via nets"), wx.DefaultPosition, wx.DefaultSize, 0 )
        subsubSizer1.Add( self.chkUpdateViaNet, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( subSizer1.GetStaticBox(), wx.ID_ANY, _(u"Track to via clearance (mm):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        subsubSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.txtTrackToViaClearance = wx.TextCtrl( subSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        subsubSizer1.Add( self.txtTrackToViaClearance, 0, wx.ALL, 5 )

        self.chkUseZoneClearance = wx.CheckBox( subSizer1.GetStaticBox(), wx.ID_ANY, _(u"Automatically use zone clearance"), wx.DefaultPosition, wx.DefaultSize, 0 )
        subsubSizer1.Add( self.chkUseZoneClearance, 0, wx.ALL, 5 )


        subSizer1.Add( subsubSizer1, 1, wx.EXPAND, 5 )


        mainSizer.Add( subSizer1, 1, wx.EXPAND, 5 )

        subSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Via settings") ), wx.VERTICAL )

        subsubSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
        subsubSizer2.SetFlexibleDirection( wx.BOTH )
        subsubSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText3 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Pre-defined sizes (mm):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText3, 0, wx.ALL, 5 )

        lstDefinedViaSizesChoices = []
        self.lstDefinedViaSizes = wx.Choice( subSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstDefinedViaSizesChoices, 0 )
        self.lstDefinedViaSizes.SetSelection( 0 )
        subsubSizer2.Add( self.lstDefinedViaSizes, 0, wx.ALL, 5 )

        self.m_staticText4 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Via type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText4, 0, wx.ALL, 5 )

        lstViaTypeChoices = []
        self.lstViaType = wx.Choice( subSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstViaTypeChoices, 0 )
        self.lstViaType.SetSelection( 0 )
        subsubSizer2.Add( self.lstViaType, 0, wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Via diameter (mm):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.txtViaDiameter = wx.TextCtrl( subSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        subsubSizer2.Add( self.txtViaDiameter, 0, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Start layer:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText6, 0, wx.ALL, 5 )

        lstStartLayerChoices = []
        self.lstStartLayer = wx.Choice( subSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstStartLayerChoices, 0 )
        self.lstStartLayer.SetSelection( 0 )
        subsubSizer2.Add( self.lstStartLayer, 0, wx.ALL, 5 )

        self.m_staticText7 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Via hole (mm):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.txtViaHole = wx.TextCtrl( subSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        subsubSizer2.Add( self.txtViaHole, 0, wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"End layer:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText8, 0, wx.ALL, 5 )

        lstEndLayerChoices = []
        self.lstEndLayer = wx.Choice( subSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstEndLayerChoices, 0 )
        self.lstEndLayer.SetSelection( 0 )
        subsubSizer2.Add( self.lstEndLayer, 0, wx.ALL, 5 )


        subsubSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        subsubSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( subSizer2.GetStaticBox(), wx.ID_ANY, _(u"Annular rings:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        subsubSizer2.Add( self.m_staticText9, 0, wx.ALL, 5 )

        lstAnnularRingsChoices = []
        self.lstAnnularRings = wx.Choice( subSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, lstAnnularRingsChoices, 0 )
        self.lstAnnularRings.SetSelection( 0 )
        subsubSizer2.Add( self.lstAnnularRings, 0, wx.ALL, 5 )


        subSizer2.Add( subsubSizer2, 1, wx.EXPAND, 5 )


        mainSizer.Add( subSizer2, 1, wx.EXPAND, 5 )

        subSizer3 = wx.BoxSizer( wx.HORIZONTAL )


        subSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        subsubSizer3 = wx.StdDialogButtonSizer()
        self.subsubSizer3Apply = wx.Button( self, wx.ID_APPLY )
        subsubSizer3.AddButton( self.subsubSizer3Apply )
        self.subsubSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
        subsubSizer3.AddButton( self.subsubSizer3Cancel )
        subsubSizer3.Realize()

        subSizer3.Add( subsubSizer3, 1, wx.EXPAND, 5 )


        mainSizer.Add( subSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.lstViaNet.Bind( wx.EVT_CHOICE, self.lstViaNetOnChoice )
        self.chkUpdateViaNet.Bind( wx.EVT_CHECKBOX, self.chkUpdateViaNetOnCheckBox )
        self.txtTrackToViaClearance.Bind( wx.EVT_TEXT, self.txtTrackToViaClearanceOnText )
        self.chkUseZoneClearance.Bind( wx.EVT_CHECKBOX, self.chkUseZoneClearanceOnCheckBox )
        self.lstDefinedViaSizes.Bind( wx.EVT_CHOICE, self.lstDefinedViaSizesOnChoice )
        self.lstViaType.Bind( wx.EVT_CHOICE, self.lstViaTypeOnChoice )
        self.txtViaDiameter.Bind( wx.EVT_TEXT, self.txtViaDiameterOnText )
        self.lstStartLayer.Bind( wx.EVT_CHOICE, self.lstStartLayerOnChoice )
        self.txtViaHole.Bind( wx.EVT_TEXT, self.txtViaHoleOnText )
        self.lstEndLayer.Bind( wx.EVT_CHOICE, self.lstEndLayerOnChoice )
        self.lstAnnularRings.Bind( wx.EVT_CHOICE, self.lstAnnularRingsOnChoice )
        self.subsubSizer3Apply.Bind( wx.EVT_BUTTON, self.subsubSizer3OnApplyButtonClick )
        self.subsubSizer3Cancel.Bind( wx.EVT_BUTTON, self.subsubSizer3OnCancelButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def lstViaNetOnChoice( self, event ):
        event.Skip()

    def chkUpdateViaNetOnCheckBox( self, event ):
        event.Skip()

    def txtTrackToViaClearanceOnText( self, event ):
        event.Skip()

    def chkUseZoneClearanceOnCheckBox( self, event ):
        event.Skip()

    def lstDefinedViaSizesOnChoice( self, event ):
        event.Skip()

    def lstViaTypeOnChoice( self, event ):
        event.Skip()

    def txtViaDiameterOnText( self, event ):
        event.Skip()

    def lstStartLayerOnChoice( self, event ):
        event.Skip()

    def txtViaHoleOnText( self, event ):
        event.Skip()

    def lstEndLayerOnChoice( self, event ):
        event.Skip()

    def lstAnnularRingsOnChoice( self, event ):
        event.Skip()

    def subsubSizer3OnApplyButtonClick( self, event ):
        event.Skip()

    def subsubSizer3OnCancelButtonClick( self, event ):
        event.Skip()


