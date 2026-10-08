# Localization i18n Agent

Plans **i18n / localization** work: locales, copy inventory, message keys, pluralization, formatting, glossary, and optional JSON catalog sketches. Optional JSON (`LocalizationI18nReply`). Multi-provider LLM.

```bash
cd "localization i18n agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "UI strings + target locales..."
```

Env: `LOCALIZATION_I18N_AGENT_PROVIDER`, `LOCALIZATION_I18N_AGENT_MODEL`. Have translators review final copy—especially legal/medical.
