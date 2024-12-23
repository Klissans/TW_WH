import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper

from battle_ui import mod_battle_ui



if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    mod_battle_ui()
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    shutil.copy2('../_lua_shared/_helpers.klissan.lua', 'output/script/_lib/mod/')
    
    MOD_NAME = '!Klissans_hui'
    OUTPUT_DIR = 'output'
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    # os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\campaign.lnk")
    # os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\dev.lnk")
    
    # List
    # CcoCustomBattlePlayerSlot
    #
    #
    # ContextCommandLeftClick
    # CcoSubcultureRecord
    # StoredContextFromParent("CcoCustomBattlePlayerSlot").SetSubculture(this)
    #
    # ContextVisibilitySetter
    # CcoCultureRecord
    # (factions = StoredContextFromParent("CcoCustomBattlePlayerSlot").FactionsForCulture(this).Filter(OwnershipProductRequirementList.IsEmpty == false)) = > {
    #     (this.Key.Contains("wh3_main_") == false | | IsOgreKingdoms) & & factions.IsEmpty == false & & factions.All(OwnershipProductRequirementList.All(OwnershipProductRecordList.Any(IsOwned == false & & IsFlc == false)))}
    #
    # # ContextLayoutTooltip
    # CcoCultureRecord
    # CcoRTOwnershipList(List: StoredContextFromParent("CcoCustomBattlePlayerSlot").FactionsForCulture(this).Transform(OwnershipProductRequirementList).Distinct)
    #
    #
    # ContextTooltipSetter
    # CcoCultureRecord
    # Loc("tooltip_content_alert")
    
    # language=javascript
    """
        (
            spell_key = StoredContextFromParent('CcoBattleAbility').SetupAbilityContext.RecordKey.Replace('_upgraded', ''),
            units_holder = Component('cards_panel').ChildContext('review_DY'),
            selected_units = units_holder.ChildList
                .Filter(ChildContext('card_image_holder').ChildContext('battle').ChildContext('smoke_particle_emitter').IsVisible)
                .Transform(ContextsList.FirstContext((x=false, _) => ContextTypeId(x) == 'CcoBattleUnit')),
            mana_cost = selected_units.Sum(AbilityList.FirstContext(RecordKey == spell_key).ManaUsed)
        ) => mana_cost
    """
    """
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            unit_type = 'commander',
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = pslot.UnitList.Filter(true).Copy()
        ) => pslot
        {
            Do(
                pslot.RecruitUnit(runit, pslot.IsRecruitingReinforcements),
                soc.SetStringValue(soc.StringValue + explain_str)
            )
        }
    (
        croot = CampaignRoot,
        faction = croot.FactionList.FirstContext(FactionRecordContext.Key == 'wh3_dlc23_chd_astragoth'),
        province_capital = faction.SettlementList.FirstContext(IsProvinceCapital),
        province_town = faction.SettlementList.FirstContext(!IsProvinceCapital)
    ) =>
    {
        GetIf(
            IsContextValid(province_capital),
            (
                military_chains = province_capital.ChainList.Filter(TechnologyCategory == 'military'),
                level_unit_pairs = military_chains
                    .Transform(LevelsList)
                    .Transform(
                        MakePair(PrimarySlotBuildingLevelRequirement, UnitList(province_capital, faction))
                    )
                    .Filter(Second.Size > 0)
            ) => {level_unit_pairs}
        )
    }
    
    ContextList
CcoBuildingLevelRecord
UnitList(Buildings.StoredSettlementOrCharacter, PlayersFaction)
(meta-event) CampaignLocalFactionChanged
    """
    # Pick General
    # language=javascript
    """
    (
        range = MakePair(0, 10)
    ) =>
    {
       Generate(range.Second - 1)
    }
    """#Generate(10, MakePair(1, 2))
    ######## CcoStaticObject().Generate(5)
    
    # language=javascript
    """
    (
        range = MakePair(1, 10)
        
    ) =>
    {
       Do(i= 111) + i + range.Second,
       Do(i = 4, c = i + 5) + GetIf(true, c+3)
    }
    """
    # MakePair(MakePair(1,2), 3) TODO: !!!!!!!
    # Generate(10, MakePair(1, 2)).Transform(First) - doesn't work :( no simple-type arrays
    # Generate(10, MakePair('1', 2)).Transform(First) - doesn't work :( no simple-type arrays
    
    """
   <!-- AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities")
    ===WORKS===
    (al = AbilityIconList, x =  AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }

    ==DOES NOT WORK==
    (al = AbilityIconList; x =  AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { al; x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x, x }
    (al = AbilityIconList, f = (x) => { x.Filter(CategoryStateName == "spells") } ) => { f(al) }
    -->
"""