CcoBattleUnit
{

  GetGoldValue(Bool is_hp_adjusted)
  {
    (
        exp_cost = GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11) ),
        al = GetIf(
            IsCharacter,
            UnitDetailsContext.AbilityDetailsList
                .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                .Filter(IsUnitUpgrade)
                .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                .Sum(AdditionalMeleeCp + AdditionalMissileCp)
        ),
        cost = UnitRecordContext.Cost + exp_cost + al
    ) =>
    {RoundFloat(GetIfElse(is_hp_adjusted, HealthPercent * cost, cost))}
  }

}