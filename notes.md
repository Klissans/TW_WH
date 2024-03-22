
For UNIString - CcoString

CompileExpression(String) -> CcoContextExpression
RetrieveSymbolsList(CcoContextExpression) -> CcoContextSymbol-List
RetrieveSymbolsList CcoContextExpression

RetrieveSymbolsList(this).At(5).EvaluateSymbol()
Try(RetrieveSymbolsList(FrontendRoot).At(5).EvaluateSymbol(FrontendRoot))
CompileExpression('CurrentMenuId').EvaluateExpression(this)
EvaluateExpression('CurrentMenuId') -- doesn't have access to local variables in lambda

* example named parameters:
```    (
        pslot = Component('recruitment_parent').ContextsList[0],
        unit_group_record = DatabaseRecordContext('CcoUiUnitGroupParentRecord', 'commander'),
        unit_list = pslot.UnitListForUnitGroupParent(unit_group_record)
    ) => unit_list.Filter((x, uc=x.UnitContext) => pslot.CanRecruitUnit(uc, pslot.IsRecruitingReinforcements))
```
(s='ToNumber(a)')=>{EvaluateExpression(s, '10')}
context -> EvaluateExpression
(a=10, f = '3 * %d') => {EvaluateExpression(Format(f, a))}
() => 1 + 2
true | 2 - alias for get-if
true | 2 | 3 - alias for get-if-else
(a = true | 1 | 2 ) => a # true :((

a || b || c

# MakePair / For-Loop
MakePair(1,2) -> CcoPair
Generate(10, MakePair(1, 2))

component -> CreateComponent

CcoComponent - SetContext | SetContextFromId | SetProperty


# Random
TrueRandomInRange(0, 10)
RandomInRange(0,10)

# Useful Misc
HasFunction
FindContext
SearchContext

StoreList(TeamList, 'list')  - to store list
FindContext('CcoContextList', 'list').List -- to retrieve the list

CcoScriptTableNode

CcoScriptObject 

ContextInitScriptObject 
script_id
script_id_expression
				<callback_with_context
					callback_id="ContextInitScriptObject"
					context_object_id="CcoStaticObject">
					<child_m_user_properties>
						<property
							name="script_id_expression"
							value="Format(&quot;follower_threshold_%d&quot;, self.ParentContext.ParentContext.ChildIndex)"/>
					</child_m_user_properties>
				</callback_with_context>
				<callback_with_context
					callback_id="ContextVisibilitySetter"
					context_object_id="CcoScriptObject"
					context_function_id="StringValue.IsEmpty == false &amp;&amp; IsContextValid(FindContext(&quot;CcoCampaignFaction&quot;, StringValue))"/>
				<callback_with_context
					callback_id="ContextStateSetter"
					context_object_id="CcoScriptObject"
					context_function_id="StringValue"/>
ScriptObjectContext("test")
	
(a = ScriptObjectContext('test').SetNumericValue(111), d1 = Do(a.SetNumericValue(111)) ) => a.NumericValue



https://chadvandy.github.io/tw_modding_resources/WH3/cco/documentation.html#context

CcoRTExpander
CcoRTExpander(&#10;        TargetComponent: context,&#10;        IsSearch: is_searching,&#10;        CloseOthers: false)

ContextStateSetter
CcoCustomBattleLobby
this | SettingsContext.IsLabMode => "lab" | IsSinglePlayer => "custom" | "mp"



				<callback_with_context
					callback_id="ComponentCreator"
					context_object_id="CcoBattleRoot">
					<child_m_user_properties>
						<property
							name="create_condition"
							value="HasSupplies"/>
						<property
							name="layout"
							value="ui/battle ui/hud_battle_reinforcement_purchase"/>

					</child_m_user_properties>
				</callback_with_context>


The damage caused by a unit's weapon, split between base and armour piercing.||Armour-piercing damage is always applied; base damage can be blocked by armour.
||Height modifier max bonus: +/-[[col:yellow]]30[[/col]]%
Max height modifier difference: +/-[[col:yellow]]1[[/col]]m

[[img:ui/skins/default/icon_stat_damage_base.png]][[/img]] Base Weapon Damage: 10
[[img:ui/skins/default/modifier_icon_armour_piercing.png]][[/img]] Armour-Piercing Weapon Damage: 24
[[img:ui/skins/default/modifier_icon_bonus_vs_large.png]][[/img]] Bonus vs. Large: 19

# ALWAYS APPLY .Replace('||', '') on unistrings !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


СcoSpecialAbilityPhaseRecord
CcoEffect





[[img:ui/skins/default/icon_stat_ranged_damage_base.png]][[/img]] Базовый урон от выстрелов: 8
[[img:ui/skins/default/modifier_icon_armour_piercing_ranged.png]][[/img]] Урон от бронебойных выстр.: 24
[[img:ui/skins/default/icon_explosive_damage.png]][[/img]] Базовый урон от взрыва: 15
[[img:ui/skins/default/icon_stat_explosive_armour_piercing_damage.png]][[/img]] Урон сквозь доспехи от взрыва: 6
[[img:ui/skins/default/modifier_icon_suppressive_fire.png]][[/img]] Burst Size: 4
[[img:ui/battle ui/ability_icons/wh2_dlc11_unit_passive_extra_powder.png]][[/img]] Number of Projectiles: 2
[[img:ui/battle ui/ability_icons/wh2_main_character_passive_darken_the_skies.png]][[/img]] Shots per Volley: 2
[[img:ui/skins/default/icon_stat_reload_time.png]][[/img]] Время перезарядки: 7.0 сек.

The damage caused by a missile attack, split between base and armour piercing.||Armour-piercing damage is always applied, base damage can be blocked by armour.
||Height modifier max bonus: +/-[[col:yellow]]30[[/col]]%
Max height modifier difference: +/-[[col:yellow]]40[[/col]]m
[[img:ui/skins/default/icon_distance_to_target.png]][[/img]][[col:yellow]]Projectile's Shockwave Radius[[/col]] - the radius of the projectile where it deals full damage. All projectiles are affected by [[img:ui/campaign ui/effect_bundles/resistance_missile.png]][[/img]]
[[col:yellow]]Penetration[[/col]] - how good the projectile at penetrating entities (see the mod's description on Steam for more info).
[[img:ui/skins/default/icon_distance_to_target.png]][[/img]][[col:yellow]]Explosion's Detonation Radius[[/col]] - the radius from the center of the projectile where explosion deals full damage. Resisted by [[img:ui/campaign ui/effect_bundles/resistance_missile.png]][[/img]]

\

# ContextInitScriptObject
		<cooldown_info
			this="E9D60DEE-927F-408D-8B587A3826095E37"
			id="cooldown_info"
			offset="0.00,64.00"
			allowhorizontalresize="false"
			tooltipslocalised="true"
			uniqueguid="E9D60DEE-927F-408D-8B587A3826095E37"
			currentstate="5FDE86C4-11E2-4522-8B54F7DC6D411B0D"
			defaultstate="5FDE86C4-11E2-4522-8B54F7DC6D411B0D">
			<callbackwithcontextlist>
				<callback_with_context
					callback_id="ContextTextLabel"
					context_object_id="CcoScriptObject"/>
				<callback_with_context callback_id="ContextInitScriptObject"/>
			</callbackwithcontextlist>
			<userproperties>
				<property
					name="different_text_per_state"
					value=""/>
				<property
					name="script_id"
					value="wanted_level_cooldown"/>
			</userproperties>
			<states>
				<newstate
					this="5FDE86C4-11E2-4522-8B54F7DC6D411B0D"
					name="NewState"
					width="310"
					height="83"
					uniqueguid="5FDE86C4-11E2-4522-8B54F7DC6D411B0D">
					<component_text
						text="[[col:yellow]]Hostility level is on cooldown, will go back to normal in: {{CcoScriptObject:RoundFloat(NumericValue)}} turns[[/col]]"



StringGet("main_units_tables_unit_wh2_dlc09_tmb_cav_skeleton_horsemen_0")



LocLanguage -> EN/RU/CN
LocalisedColonWithSpace
LocalisedCommaWithSpace


SetScriptLock
IsScriptLockActive
ScriptLockList

CampaignScriptLockChangedAny	
CampaignScriptLockChanged_



Callbacks
UI Update Messages

	core:add_listener(
		"hellforge_upkeep_modifier_unit_disbanded",
		"UnitUpgraded",
		function(context)
			local faction = context:unit():faction()
			return faction:is_human() and faction:is_contained_in_faction_set(self.faction_set_key)
		end,
		function(context)
			local faction_interface = context:unit():faction()
			cm:callback(
				function()
					self:multiply_armament_cost_per_unit(faction_interface)
				end,
				0.5
			)
		end,
		true
	)
				<callback_with_context
					callback_id="TreeCallback"
					context_object_id="CcoStaticObject"
					context_function_id="UnitUpgradeManagerContext.UnitGroupUpgradesTree(UnitUpgradeManagerContext.ForceUnitGroupUpgradesList(SelectedCharacter.MilitaryForceContext,  Component(&quot;B10C28DC-AFC1-4907-B20296FD966B63E2&quot;).UpgradingUnitsContextList.FirstContext).Filter(Category == Component(&quot;59B57F69-058B-4679-9A85EA5A71F75D35&quot;).CurrentSelectedComponents.FirstContext.ParentContext.GetProperty(&quot;God&quot;)))">
					<child_m_user_properties>
						<property
							name="event1"
							value="UnitUpgradeGroupUiInfoReloaded"/>
						<property
							name="event2"
							value="warbands_category_changed"/>
						<property
							name="event3"
							value="UnitUpgraded"/>
					</child_m_user_properties>
				</callback_with_context>


---

ContextObjectStore
CcoUiUnitGroupParentRecord
hide_if_empty, 

ContextList
CcoUiUnitGroupParentRecord
StoredContextFromParent("CcoCustomBattlePlayerSlot").UnitListForUnitGroupParent(this).Reverse
StoredContextFromParent("CcoCustomBattlePlayerSlot").UnitListForUnitGroupParent(ContextsList[0])
event0, CustomBattleOnPlayerFactionChangedPlayer
event1, CustomBattleOnSettingChangedIsUsingUnitCaps

CcoUiUnitGroupParentRecord.RecordList
ContextsList[0].UnitList.Transform(CustomBattlePermissionsContext)
ContextsList[1].UnitListForUnitGroupParent(ContextsList[0]) .Reverse


ContextListEngineItemsPerRowSetter
CcoStaticObject
GetIfElse(RootComponent.Dimensions.x > 1900, 13, 10)


# lambdas 

        Do(pslot.RecruitUnit(ContextsList.FirstContext((x) => IsOfType(x, "CcoUnitsCustomBattlePermissionRecord")), pslot.IsRecruitingReinforcements))











wh_main_chs_chaos	36090850	false