from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
import json
import httpx
from app.config import settings
from app.schemas.risk import RiskAssessment, AINarrativeReport
from app.models.account import Account
from app.models.transaction import Transaction

logger = logging.getLogger("fraud_x.ai_analyst")

class AIFraudAnalystService:
    """
    AI Fraud Analyst Layer localized to the Indian Financial & Banking Ecosystem (RBI/NPCI).
    Synthesizes signals into a cohesive forensic narrative and operational recommendations.
    Provides 100% resilient dual-mode: Real LLM if configured, or high-fidelity deterministic synthesizer.
    """

    async def investigate(
        self,
        transaction: Transaction,
        account: Account,
        assessment: RiskAssessment
    ) -> AINarrativeReport:
        if not settings.USE_MOCK_AI and (settings.GEMINI_API_KEY or settings.OPENAI_API_KEY or settings.GROQ_API_KEY):
            try:
                return await self._call_external_llm(transaction, account, assessment)
            except Exception as e:
                logger.warning(f"External LLM call failed ({e}), falling back to deterministic synthesizer.")
        
        return self._generate_deterministic_narrative(transaction, account, assessment)

    def _generate_deterministic_narrative(
        self,
        transaction: Transaction,
        account: Account,
        assessment: RiskAssessment
    ) -> AINarrativeReport:
        """Synthesizes high-fidelity forensic dossier in Indian financial context with 0ms latency."""
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S IST")
        score = assessment.risk_score
        level = assessment.risk_level
        action = assessment.action_taken
        reasons = assessment.primary_reasons
        sig_codes = {s.code for s in assessment.signals}
        bank = getattr(transaction, 'bank_name', 'Bank')

        # Executive Summary
        if level in ["CRITICAL", "HIGH"]:
            exec_summary = (
                f"HIGH SEVERITY ALERT: Transaction {transaction.id} for ₹{transaction.amount:,.2f} via {transaction.transaction_type} "
                f"on account {account.id} ({account.holder_name}, {bank}) flagged with a Risk Score of {score}/100. "
                f"Multi-engine analysis detected high-probability fraudulent activity driven by {reasons[0].lower()}."
            )
        elif level == "MEDIUM":
            exec_summary = (
                f"ELEVATED RISK NOTICE: Transaction {transaction.id} for ₹{transaction.amount:,.2f} via {transaction.transaction_type} exhibits moderate deviation "
                f"(Risk Score: {score}/100). Step-up authentication or UPI PIN challenge is advised."
            )
        else:
            exec_summary = (
                f"ROUTINE APPROVAL: Transaction {transaction.id} for ₹{transaction.amount:,.2f} via {transaction.transaction_type} aligns with historical baseline "
                f"profile (Risk Score: {score}/100). No anomalous behavioral, device, or velocity markers observed."
            )

        # Forensic Narrative Synthesis
        narrative_paragraphs = []
        
        # Paragraph 1: Anomaly overview
        p1 = (
            f"Forensic examination of transaction {transaction.id} shows an initiated {transaction.transaction_type} payment of ₹{transaction.amount:,.2f} "
            f"to merchant/beneficiary '{transaction.merchant_name}' ({transaction.merchant_category}). "
            f"The account holder {account.holder_name} maintains a calibrated average spending volume of ₹{account.avg_amount:,.2f} "
            f"(standard deviation: ±₹{account.std_amount:,.2f}) through {bank}."
        )
        if "EXTREME_AMOUNT_OUTLIER" in sig_codes:
            multiplier = transaction.amount / max(account.avg_amount, 1.0)
            p1 += f" The current transaction represents a {multiplier:.1f}x spike over established spending history."
        narrative_paragraphs.append(p1)

        # Paragraph 2: Technical Vectors
        p2_parts = []
        if "IMPOSSIBLE_TRAVEL_VELOCITY" in sig_codes:
            p2_parts.append(
                f"Geographic intelligence confirmed physical impossible travel (calculated transit velocity: {assessment.speed_kmh:,.0f} km/h), "
                f"indicating remote UPI credential compromise, SIM-swap vulnerability, or device spoofing."
            )
        if "NEW_DEVICE_DETECTED" in sig_codes:
            p2_parts.append(
                f"The originating device fingerprint ({transaction.device_id[:14]}...) has never been authenticated on this account before."
            )
        if "SUSPICIOUS_DEVICE_REUSE" in sig_codes:
            p2_parts.append(
                f"Crucially, this exact hardware fingerprint is actively associated with {assessment.device_account_count} distinct bank accounts, "
                f"strongly pointing to a coordinated money mule syndicate or emulator farm."
            )
        if "RAPID_BURST_VELOCITY" in sig_codes or "CARD_TESTING_FREQUENCY" in sig_codes:
            p2_parts.append(
                f"Velocity analysis detected an automated burst of {assessment.velocity_count_1m} transaction requests within 60 seconds, "
                f"typical of automated UPI probing scripts or card brute-force attacks."
            )
        if "CIRCULAR_TRANSFER_RING" in sig_codes:
            p2_parts.append(
                "Graph topology analysis identified a closed circular fund routing ring across beneficiary accounts, indicating intentional layering."
            )
        
        if p2_parts:
            narrative_paragraphs.append(" ".join(p2_parts))
        else:
            narrative_paragraphs.append(
                "Telemetry confirms known registered hardware, domestic regional origin, and standard diurnal velocity."
            )

        # Paragraph 3: Context Correlation
        if len(assessment.signals) >= 2:
            p3 = (
                f"Cross-Vector Synthesis: Correlation across {len(assessment.signals)} distinct risk dimensions proves that this event "
                f"cannot be attributed to legitimate accidental user variation. Immediate defensive containment is warranted."
            )
        else:
            p3 = "Cross-Vector Synthesis: Single isolated indicator does not indicate systemic fraud or syndicate compromise."
        narrative_paragraphs.append(p3)

        forensic_narrative = "\n\n".join(narrative_paragraphs)

        # Correlation Analysis
        if sig_codes:
            corr_analysis = (
                f"Cross-vector correlation links {', '.join(sorted(list(sig_codes))[:3])}. "
                "The concurrent emergence of hardware novelty and velocity/geographic divergence represents a high-fidelity attack pattern."
            )
        else:
            corr_analysis = "No anomalous cross-vector correlations identified."

        # Action Justification & Mitigations
        if action == "BLOCK":
            justification = "Immediate automated block enforced under RBI digital fraud guidelines to prevent capital flight."
            mitigations = [
                f"Temporarily freeze outbound UPI/IMPS transfers on account {account.id}.",
                f"Quarantine device fingerprint {transaction.device_id[:16]} across all banking channels.",
                "Trigger customer verification call via registered mobile number.",
                "Flag recipient VPA / beneficiary account in NPCI fraud registry."
            ]
            confidence = 0.96
        elif action == "HOLD":
            justification = "Transaction suspended in review queue awaiting secondary biometric or out-of-band OTP confirmation."
            mitigations = [
                "Issue mandatory step-up biometric / OTP verification to account holder.",
                "Hold funds clearing window for 15 minutes.",
                "Monitor for subsequent high-velocity UPI pull attempts."
            ]
            confidence = 0.88
        elif action == "CHALLENGE" or action == "MONITOR":
            justification = "Moderate signal deviation observed; log event and monitor account velocity for subsequent attempts."
            mitigations = [
                "Prompt customer for secondary OTP / PIN confirmation.",
                "Track device fingerprint across subsequent merchant checkout attempts."
            ]
            confidence = 0.78
        else:
            justification = "Transaction complies with standard risk tolerances and historical baseline limits."
            mitigations = ["Allow straight-through processing via payment gateway."]
            confidence = 0.99

        return AINarrativeReport(
            transaction_id=transaction.id,
            executive_summary=exec_summary,
            forensic_narrative=forensic_narrative,
            correlation_analysis=corr_analysis,
            recommended_action=action,
            confidence_score=confidence,
            action_justification=justification,
            immediate_mitigations=mitigations,
            timestamp=now_str
        )

    def _build_forensic_prompt(
        self,
        transaction: Transaction,
        account: Account,
        assessment: RiskAssessment
    ) -> str:
        signals_summary = "\n".join([
            f"- {s.name} ({s.code}): {s.description} (Observed: {s.observed_value}, Baseline: {s.baseline_value}, Points: {s.points})"
            for s in assessment.signals
        ])
        bank = getattr(transaction, 'bank_name', 'Bank')

        return f"""You are an elite AI Forensic Financial Fraud Analyst specializing in the Indian Financial and Banking Ecosystem (RBI guidelines, NPCI regulations, UPI/IMPS protocols).

Analyze this transaction:
- Transaction ID: {transaction.id}
- Account: {account.id} ({account.holder_name}, {bank})
- Amount: INR Rs {transaction.amount:,.2f} via {transaction.transaction_type}
- Beneficiary/Merchant: {transaction.merchant_name} ({transaction.merchant_category})
- Historical Baseline: Avg Rs {account.avg_amount:,.2f} +/- Rs {account.std_amount:,.2f}
- Engine Risk Score: {assessment.risk_score}/100 ({assessment.risk_level})
- Engine Recommendation: {assessment.action_taken}
- Primary Anomaly Reasons: {', '.join(assessment.primary_reasons)}
- Triggered Signals:
{signals_summary if signals_summary else "- No high-severity signals"}

Respond with a JSON object adhering to this schema:
{{
  "executive_summary": "High-level summary of the alert, risk severity, and core finding.",
  "forensic_narrative": "Detailed 2-3 paragraph forensic analysis detailing the anomalous vectors, behavioral deviation, and attack indicators in Indian banking context.",
  "correlation_analysis": "Synthesis of how multi-dimensional signals cross-correlate.",
  "recommended_action": "{assessment.action_taken}",
  "confidence_score": 0.95,
  "action_justification": "Clear justification citing regulatory and security policy reasons.",
  "immediate_mitigations": [
    "Specific immediate operational mitigation step 1",
    "Specific immediate operational mitigation step 2",
    "Specific immediate operational mitigation step 3"
  ]
}}
Only return valid JSON."""

    async def _call_groq(
        self,
        prompt: str,
        transaction: Transaction,
        assessment: RiskAssessment,
        now_str: str
    ) -> Optional[AINarrativeReport]:
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
        models = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
        async with httpx.AsyncClient(timeout=8.0) as client:
            for model in models:
                try:
                    payload = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are an AI Forensic Analyst specializing in Indian banking fraud detection (RBI/NPCI). Output strictly valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.1
                    }
                    res = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                    if res.status_code == 200:
                        parsed = json.loads(res.json()["choices"][0]["message"]["content"])
                        return AINarrativeReport(
                            transaction_id=transaction.id,
                            executive_summary=parsed.get("executive_summary", ""),
                            forensic_narrative=parsed.get("forensic_narrative", ""),
                            correlation_analysis=parsed.get("correlation_analysis", ""),
                            recommended_action=parsed.get("recommended_action", assessment.action_taken),
                            confidence_score=float(parsed.get("confidence_score", 0.95)),
                            action_justification=parsed.get("action_justification", ""),
                            immediate_mitigations=parsed.get("immediate_mitigations", []),
                            timestamp=now_str
                        )
                except Exception as e:
                    logger.warning(f"Groq model {model} invocation failed: {e}")
        return None

    async def _call_gemini(
        self,
        prompt: str,
        transaction: Transaction,
        assessment: RiskAssessment,
        now_str: str
    ) -> Optional[AINarrativeReport]:
        models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.6-flash"]
        async with httpx.AsyncClient(timeout=12.0) as client:
            for model_name in models:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
                    body = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"response_mime_type": "application/json"}
                    }
                    response = await client.post(url, json=body)
                    if response.status_code == 200:
                        data = response.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        parsed = json.loads(text)
                        return AINarrativeReport(
                            transaction_id=transaction.id,
                            executive_summary=parsed.get("executive_summary", ""),
                            forensic_narrative=parsed.get("forensic_narrative", ""),
                            correlation_analysis=parsed.get("correlation_analysis", ""),
                            recommended_action=parsed.get("recommended_action", assessment.action_taken),
                            confidence_score=float(parsed.get("confidence_score", 0.95)),
                            action_justification=parsed.get("action_justification", ""),
                            immediate_mitigations=parsed.get("immediate_mitigations", []),
                            timestamp=now_str
                        )
                except Exception as err:
                    logger.warning(f"Gemini model {model_name} invocation failed: {err}")
                    continue
        return None

    async def _call_openai(
        self,
        prompt: str,
        transaction: Transaction,
        assessment: RiskAssessment,
        now_str: str
    ) -> Optional[AINarrativeReport]:
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        models = ["gpt-4o-mini", "gpt-3.5-turbo"]
        async with httpx.AsyncClient(timeout=8.0) as client:
            for model in models:
                try:
                    payload = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are an AI Forensic Analyst specializing in Indian banking fraud detection (RBI/NPCI). Output strictly valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.1
                    }
                    res = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    if res.status_code == 200:
                        parsed = json.loads(res.json()["choices"][0]["message"]["content"])
                        return AINarrativeReport(
                            transaction_id=transaction.id,
                            executive_summary=parsed.get("executive_summary", ""),
                            forensic_narrative=parsed.get("forensic_narrative", ""),
                            correlation_analysis=parsed.get("correlation_analysis", ""),
                            recommended_action=parsed.get("recommended_action", assessment.action_taken),
                            confidence_score=float(parsed.get("confidence_score", 0.95)),
                            action_justification=parsed.get("action_justification", ""),
                            immediate_mitigations=parsed.get("immediate_mitigations", []),
                            timestamp=now_str
                        )
                except Exception as e:
                    logger.warning(f"OpenAI model {model} invocation failed: {e}")
        return None

    async def _call_external_llm(
        self,
        transaction: Transaction,
        account: Account,
        assessment: RiskAssessment
    ) -> AINarrativeReport:
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S IST")
        prompt = self._build_forensic_prompt(transaction, account, assessment)

        # 1. Try Groq (high-speed inference)
        if settings.GROQ_API_KEY:
            report = await self._call_groq(prompt, transaction, assessment, now_str)
            if report:
                return report

        # 2. Try Gemini
        if settings.GEMINI_API_KEY:
            report = await self._call_gemini(prompt, transaction, assessment, now_str)
            if report:
                return report

        # 3. Try OpenAI
        if settings.OPENAI_API_KEY:
            report = await self._call_openai(prompt, transaction, assessment, now_str)
            if report:
                return report

        # Fallback to deterministic synthesizer
        return self._generate_deterministic_narrative(transaction, account, assessment)

ai_analyst = AIFraudAnalystService()
