CcoBattleUnit
{

  GetGoldValue(Bool is_hp_adjusted)
  {
    (
        base_cost = UnitRecordContext.Cost
        + GetIf(UnitRecordContext.Key == 'wh3_dlc24_tze_cha_changeling', UnitDetailsContext.AbilityDetailsList.FirstContext(Key == 'wh3_dlc24_lord_abilities_formless_horror').AbilityContext.SpawnedMainUnitRecordContext.Cost)
        + GetIf(UnitRecordContext.Key == 'wh3_dlc24_tze_cha_blue_scribes', 700 + 1500),
        exp_cost = GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11) ),
        al = GetIf(
            IsCharacter,
            GetIfElse(
                UnitRecordContext.Key == 'wh3_dlc24_tze_cha_blue_scribes',
                GetIf(IsContextValid(UnitDetailsContext.AbilityIconList.FirstContext(Key == 'wh3_dlc24_hero_passive_spell_syphon')), 180),
                UnitDetailsContext.AbilityDetailsList
                    .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                    .Filter(IsUnitUpgrade)
                    .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                    .Sum(AdditionalMeleeCp + AdditionalMissileCp)
            )
        ),
        cost = base_cost + exp_cost + al
    ) =>
    {RoundFloat(GetIfElse(is_hp_adjusted, HealthPercent * cost, cost))}
  }

}