CcoCampaignMilitaryForce
{

  GetBundlesEffects(Bool as_string)
  {
        (
            effects = EffectBundleUnfilteredList.Transform(EffectsIncludingHiddenList)
                .Filter(StringContains(EffectScopeContext.Key, 'to_force_own') || StringContains(EffectScopeContext.Key, 'to_parent_army_own')),
            effects_str = effects.JoinString(Format('%s,%d', EffectKey, Value), ';')
        ) => GetIfElse(as_string, effects_str, effects)
  }
  
  GetSkillsEffects(Bool as_string)
  {
        (
            chars_skill_effects = CharacterList.Transform(SkillList).Transform(EffectUnfilteredList)
                .Filter(StringContains(EffectScopeContext.Key, 'to_force_own') || StringContains(EffectScopeContext.Key, 'to_parent_army_own') || EffectKey == 'wh_main_effect_agent_movement_range_mod'),
            skill_effects_str = chars_skill_effects.JoinString(Format('%s,%d', EffectKey, Value), ';')
        ) => GetIfElse(as_string, skill_effects_str, chars_skill_effects)
  }

  GetTraitsEffects(Bool as_string)
  {
        (
            chars_traits_effects = CharacterList.Transform(TraitsList).Transform(EffectUnfilteredList)
                .Filter(StringContains(EffectScopeContext.Key, 'to_force_own') || StringContains(EffectScopeContext.Key, 'to_parent_army_own')),
            effects_str = chars_traits_effects.JoinString(Format('%s,%d', EffectKey, Value), ';')
        ) => GetIfElse(as_string, effects_str, chars_traits_effects)
  }

  GetBackgroundEffects(Bool as_string)
  {
        (
            chars_skill_effects = CharacterList.Transform(BackgroundSkillContext).Transform(EffectUnfilteredList)
                .Filter(StringContains(EffectScopeContext.Key, 'to_force_own') || StringContains(EffectScopeContext.Key, 'to_parent_army_own')),
            skill_effects_str = chars_skill_effects.JoinString(Format('%s,%d', EffectKey, Value), ';')
        ) => GetIfElse(as_string, skill_effects_str, chars_skill_effects)
  }

  GetAncillaryEffects(Bool as_string)
  {
        (
            chars_skill_effects = CharacterList.Transform(AncillaryList).Transform(EffectUnfilteredList)
                .Filter(StringContains(EffectScopeContext.Key, 'to_force_own') || StringContains(EffectScopeContext.Key, 'to_parent_army_own')),
            skill_effects_str = chars_skill_effects.JoinString(Format('%s,%d', EffectKey, Value), ';')
        ) => GetIfElse(as_string, skill_effects_str, chars_skill_effects)
  }

  GetAllEffectsAsString()
    {
        GetBundlesEffects(true) + ';' + GetSkillsEffects(true)  + ';' + GetTraitsEffects(true) + ';' + GetBackgroundEffects(true) + ';' + GetAncillaryEffects(true)
    }
}