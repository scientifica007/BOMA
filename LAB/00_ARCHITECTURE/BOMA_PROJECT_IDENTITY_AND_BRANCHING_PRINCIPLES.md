# BOMA — هوية المشروع ومبادئ البناء المتفرع

**الاسم:** Branch Oriented Math (BOMA) — الرياضيات الموجّهة بالتفرّع  
**التاريخ:** 30 أكتوبر 2026  
**المصدر:** توضيحات مباشرة من مالك المشروع بشأن غايته، وعلاقة اللبنة الأصلية ببديلها، ودور النتائج غير الناجحة، والتمييز بين هوية المشروع وبرنامج اختباره.  
**طبيعة الوثيقة:** شرح مفاهيمي مرجعي للبشر والأنظمة الذكية، وليس خطة تجربة مجمدة ولا ترخيصاً لتنفيذ أبحاث أو تغيير حوكمة القبول.

## 1. BOMA في أقل من دقيقة

**BOMA مشروع لتطوير منظومة تسمح ببناء رياضيات شفافة، قابلة للتتبع والتحقق والتوثيق والتفريع.**

يُنشئ الباحث لبنات وكتلاً رياضية على جذور وفرضيات معلنة، ويمكنه أن يفتح، عند أي موضع مناسب، فرعاً بنائياً جديداً بسبب تغيير محدد. لا يُعدّل هذا التفرّع البناء الأصلي: يولد بديل جديد يتأسس على الجذور التي يحتاجها، ثم يُتاح له التطور إلى نتائج قد تكون مألوفة أو غير متوقعة أو جديدة. لا يشترط أن يقلد الفرع الأصل أو يقارن نفسه به أو يلتقي معه.

ويحفظ BOMA المعرفة المتولدة في المسارات الناجحة والجزئية والمتعثرة والفاشلة، مع بيان حدود كل نتيجة والنزاهة في ادعاء ما ثبت وما لم يثبت. وطموحه الأعلى إتاحة اكتشاف أو ابتكار رياضي أصيل؛ وتبقى له قيمة علمية ومنهجية وبيداغوجية حتى لو لم ينتج اكتشافاً غير مسبوق.

**لا يُعرّف BOMA بأنه مشروع «يبدأ من المعروف».** إعادة بناء الأعداد الطبيعية والصحيحة والنسبية والحقيقية والمركبة هي **استراتيجية معايرة واختبار مختارة** لآلة بناء الرياضيات؛ ليست هوية الآلة، وليست شرطاً عاماً على مدخلاتها أو مخرجاتها.

## 2. المثال البنائي الحاسم: A، B، B′

إذا كان البناء الأصلي:

```text
جذور معلنة R
      │
      ▼
      A
      │
      ▼
      B  ─────► C
```

وأردنا تجربة تغيير متعلق باللبنة B، **فلا نستبدل B في مكانها ولا نُجبر B′ على الاشتقاق من B**؛ بل نفرّع من الأساس البنائي المناسب، مثلاً A:

```text
       جذور معلنة R
             │
             A
          ┌──┴─────────┐
          ▼            ▼
      B الأصلية     B′ البديلة
          │            │
          ▼            ▼
          C            C′ ──► D′ ──► ...
```

**نقطة دقيقة:** تشير B الأصلية إلى *مرجع التغيير ومصدر السؤال البحثي*، بينما تحدد أسهم A→B وA→B′ *الاعتماد البنائي أو الرياضي*. ومن الممكن أن تربط B وB′ علاقة رياضية مثبتة، وقد لا توجد علاقة مثبتة بينهما، وقد تكون العلاقة مجهولة أو غير ذات صلة بسؤال البحث. لا يُستنتج أي سهم `B → B′` من مجرد تسمية «تغيير B». وإذا احتاج B′ بعض نتائج B فعلاً، يُسجل ذلك صراحة بوصفه تبعية إضافية، لا فرضاً خفياً.

ولا تعني عبارة «العودة إلى A» فرض خط مستقيم في كل حالة: فقد تعتمد B أو B′ على مجموعة من اللبنات أو مسارات متوازية أخرى. الواجب هو إعلان **مجموعة الأسس الفعلية للفرع الجديد وإمكان تتبعها إلى الجذور المصرّح بها**. وقد يقتضي تغيير جذري مختلف إعلان جذور أو مسلمات جديدة؛ يجب حينئذ إظهار هذا التحول وعدم ادعاء أنه اشتُق من جذور لم تعد تكفي.

التفرّع البنائي علاقة في **خريطة الرياضيات (Construction DAG)** وليس هو نفسه إنشاء `Git branch` في المستودع. فرع Git أداة عمل وتتبع لإصدارات الملفات؛ أما الفرع الرياضي فله تعريفاته وفرضياته وبراهينه ونسبه البنائي الخاص.

## 3. منهجان مشروعان ومستقلان

**أ. بناء فرع جديد واستكشافه (Branch-first construction).** يبدأ بتغيير مضبوط يُنشئ B′ على أساس معلن، ثم يبني الباحث C′ وما يليها ليرى ما قد يظهر. المقارنة مع B أو C أو إعادة الالتقاء معها **اختيارية**؛ ليست شرطاً للصحة أو قيمة الفرع. لا تُفرض بنية نتيجة نهائية متوقعة مسبقاً.

**ب. تحليل أثر التغيير (Change-impact investigation).** يختار الباحث دراسة ما قد يتأثر إذا تغير عنصر، عبر التبعيات الأمامية أو الخلفية أو الجانبية، المباشرة أو غير المباشرة، المعلنة أو المكتشفة أثناء العمل. وقد تُستخدم فروع مستقلة لتجريب هذا الأثر، دون تعديل الأصل.

قد يجتمع المنهجان أو يتعاقبان، لكن **BOMA لا يُختزل في تحليل آثار التغيير على المسار القائم**. وأي مقارنة أو تماثل أو إعادة التقاء بين مسارين تتطلب برهاناً مستقلاً حين يُدّعى تحققها، ولا تُفرض على كل فرع.

## 4. شرط التماسك البنائي حتى الجذور

لكل فرع جديد يجب أن نستطيع الإجابة، بالمستوى المناسب لسؤاله العلمي، عن:

1. ما نقطة التفرع ومرجع التغيير؟ وما اللبنة أو العلاقة أو الفرضية التي صيغت بطريقة أخرى؟
2. ما الجذور واللبنات والفرضيات التي *يعتمد عليها الفرع الجديد فعلياً*؟ وهل تختلف عن أصل الفرع الآخر؟
3. ما التعريفات الجديدة؟ وهل هي جيدة التكوين ومتسقة مع الفرضيات المعلنة؟ وما الذي ثَبَت وما الذي ما زال اقتراحاً؟
4. كيف يمكن إعادة إنتاج كل برهان، مع تمييز الضرورة الرياضية من اعتماد البرهان أو التنفيذ الحالي؟
5. ما علاقة الفرع بالأصل إن كانت قد دُرست؟ وما الذي لم يُفحص بعد؟

الاتصال بالجذور يعني **نسباً بنائياً وبرهانياً قابلاً للتدقيق**، لا اشتراط التطابق مع الأصل. ولا يجوز احتساب نتيجة افتراضية أو غير متحققة على أنها برهان مكتمل. كما لا يُدّعى اتساق مطلق لمجرد قبول نظام الإثبات لصياغة تستند إلى فرضيات معلنة؛ يُصرّح بنطاق التحقق وحدوده.

## 5. المجهول والاكتشاف والاختراع

**الطموح الأعلى:** أن تتيح الفروع الحرة المنضبطة ظهور خصائص أو علاقات أو إنشاءات أو نظريات أو طرق إثبات لم تكن متوقعة، وقد تصل إلى اكتشاف أو ابتكار رياضي جديد.

لا يُشترط أن تبدأ كل مهمة من منظومة معروفة، ولا أن تكون نهاية كل فرع معروفة، ولا أن يتفوق الفرع على الأصل. لكن **الجِدّة داخل المستودع لا تساوي الأصالة على مستوى الأدبيات الرياضية**؛ إعلان «اكتشاف غير مسبوق» يحتاج إلى إثبات، ومراجعة أدبيات، وتقييم مستقل مناسب.

الغاية الاستكشافية لا تُسوغ اختلاق نتيجة أو إخفاء أثر غير مرغوب فيه أو تغيير المعيار أثناء التجربة من دون تفويض وتوثيق.

## 6. الفروع التي لا تحقق الهدف تبقى معرفة

يُحتفظ بأدلة الفروع التي:
- نجحت وبلغت نتيجة مثبتة؛
- كشفت نتيجة جزئية أو حدوداً أو فرضيات إضافية؛
- توقفت لأن برهاناً لم يُستكمل؛
- كشفت تناقضاً أو مثالاً مضاداً في نطاق محدد؛
- أخفقت تقنياً في الملفات أو الأدوات أو التجميع؛
- انقطعت لأسباب تتعلق بالوقت أو الحوكمة أو تغيير الأولويات.

يُسجل لكل منها سؤال البداية، الفرضيات، التغييرات، المحاولات، الأدلة، النتائج المعروفة، والمجهول المتبقي. **تعذر إكمال برهان ≠ إثبات استحالة رياضية؛ وفشل أداة ≠ دحض فرضية؛ واجتياز الاختبارات ≠ إنجاز كل مطالب البحث أو القبول.** يمكن حفظ فرع للاستفادة البحثية والبيداغوجية حتى إن لم يصبح المسار المقبول أو لم يبلغ هدفه.

## 7. قيمة BOMA حتى دون اكتشاف رياضي غير مسبوق

يقوم المشروع أيضاً بدور بيداغوجي ومنهجي: يجعل المتعلم أو الباحث يرى كيف تتولد المفاهيم، وكيف تُختار الفرضيات، وكيف يُفتح فرع، وكيف تؤثر القرارات في النتائج، وكيف تُدرس الأخطاء والفروع المتعثرة من دون مسح تاريخها. هذه القيمة قائمة بذاتها ولا تتوقف على إثبات أصالة نتيجة جديدة عالمياً.

## 8. ماذا يعني البناء الحالي من N إلى C؟

بناء الأعداد الطبيعية `N` والصحيحة `Z` والنسبية `Q` والحقيقية `R` والمركبة `C` هو **ميدان اختبار ومعايرة معروف المواصفات**. يسمح بقياس قدرة المنظومة على البناء والتحقق والتتبع والتفرع والمقارنة؛ ولا يحصر مجال عمل BOMA في هذه المجالات.

تجارب المسارات البديلة للأعداد الحقيقية (ديدكيند/كوشي) والمركبة (P/Q)، وتجارب التبعيات، تصلح شواهد لما اختُبر حتى الآن؛ وليست تعريفاً مقيداً لما يجوز أن تدرسه المنظومة مستقبلاً.

**الوضع الفعلي والزمني لا يؤخذ من هذه الوثيقة المفاهيمية:** اقرأ `LAB/PDSA/STATUS.md` وحالة GitHub الحية وفرع/PR البحث المعني والقرارات الأحدث. بتاريخ 2026-10-30، يحتفظ PR #33 بسجل أرشفة جزئية للتجربة 016، دون إغلاق علمي أو تغيير المقبول في `main`. لا تُساوى مسودة PR بواقع مصدر `main`.

## 9. مبادئ نزاهة لا تنازل عنها

- لا تغيير صامت في اللبنة الأصلية أو تاريخ فرع آخر أو جذوره؛ الفروع مستقلة في التتبع والتقييم.
- لا تبعية صامتة ولا افتراض غير معلن؛ تُميَّز **علاقة منشأ التغيير** عن **علاقة الاعتماد البرهاني** وعن **علاقة المقارنة أو التماثل**.
- لا مساواة بين فرع بحثي وقرار `SELECTS` أو `ACCEPTED`؛ ولا قبول تلقائي بمجرد النجاح أو وجود البديل.
- لا اشتراط للمقارنة أو العودة إلى المسار الأصلي أو إعادة الالتقاء، ما لم يفرضه سؤال بحثي مختار.
- لا حجب للفروع غير الناجحة ولا لتاريخ الأخطاء والتصحيحات؛ تُصنَّف النتائج العلمية والتقنية والإدارية كل في بابها.
- لا خلط بين صحة البرهان، وتحقق المعنى المقصود، وكفاية الفرضيات، والأصالة العلمية.
- لا ادعاء باكتشاف جديد من غير تدقيق للأصالة خارج المستودع.
- لا بدء بحث ولا تغيير قبول ولا دمج PR ولا استئناف آلي من هذه الوثيقة وحدها.

## 10. للقراء ولأي نظام ذكاء اصطناعي

قبل تلخيص BOMA أو اقتراح تجربة، افصل دائماً بين:

**(1)** هوية المنظومة العامة؛ **(2)** ميدان الاختبار الحالي؛ **(3)** البناء الرياضي المقبول؛ **(4)** الفروع الاستكشافية والبدائل؛ **(5)** النتائج المثبتة والجزئية والمتعثرة؛ **(6)** ما تسمح به حوكمة التنفيذ حالياً.

لا تبدأ وصف المشروع بعبارة «BOMA يبدأ من المعروف»؛ ذلك يصف **معايرة مختارة** لا ماهيته. لا تفترض أن B′ تعتمد على B. لا تفترض أن كل تفرع يجب أن يتحد مع الأصل. لا تساوِ نتيجة جزئية مكتوبة في PR بنتيجة مقبولة على `main`.

للمستندات المختصة: `README.md` (الدخول)، `AGENTS.md` (سلوك المساعد)، `LAB/00_ARCHITECTURE/ARCHITECTURE.md` و`CONSTRUCTION_TOPOLOGY.md` (وحدات البناء والتبعيات)، `LAB/BOMA_PDSA_GOVERNANCE_AND_PDCA_LEGACY_CORRECTION_2026-08-18.md` (التعلم من التجربة)، `LAB/PDSA/STATUS.md` والحوكمة التفاعلية المؤرخة 2026-10-29 (السلطة والوضع الحالي). 

**حدود هذه الوثيقة:** توضيح هوية المشروع لا يُنشئ وحدات أو فروعاً رياضية مقبولة، ولا يغيّر Frozen Plan أو معنى `SELECTS` أو معايير القبول أو السلطات التنفيذية. أي تغيير لاحق في الإجراءات أو البنى يخضع لتفويض مستقل.


---

# BOMA — Project Identity and Branch-Oriented Mathematical Construction

**Name:** Branch Oriented Math (BOMA).  
**Date:** 2026-10-30.  
**Provenance:** Direct owner clarification of BOMA's purpose, branching semantics, the value of unsuccessful branches, and the separation of project identity from its calibration strategy.  
**Scope:** A human- and AI-readable conceptual reference, **not** a frozen experiment plan, authorization to run research, change to acceptance, or replacement for binding governance.

## 1. A one-minute explanation

**BOMA is a project to develop a system for constructing mathematics with transparency, traceability, verifiability, documentation and genuine branching.**

A researcher constructs mathematical units from explicit roots and assumptions. At a chosen point, a controlled change can give rise to a **new mathematical branch**. The existing construction is not overwritten. The alternative is established on its actual required foundations and can develop independently. It need not reproduce, outperform, be compared with, be equivalent to, or eventually reconverge with the original. Its results can be familiar, unexpected, or genuinely new.

BOMA records what is learned from successful, partial, failed, inconclusive, and technically interrupted branches alike. A highest aspiration is enabling original mathematical discovery or invention, but scientific, methodological, and pedagogical value remains even without unprecedented discoveries.

**“Starting from known mathematics” is NOT BOMA's defining purpose or a mandatory starting point.** Building natural, integer, rational, real and complex numbers is a deliberate **calibration and evaluation strategy**: testing a general-purpose mathematical construction system on outputs whose specifications are already understood. The test products do not define or limit the machine.

## 2. Precise branching: A → B and A → B′

Suppose a construction has roots `R` and units `A → B → C`. A change *motivated by* B can introduce B′, but B′ must not be silently declared to depend on B:

```text
  declared roots R
         |
         A
      /     \
     B       B′
     |       |
     C       C′ ---> D′ ---> ...
```

**Two distinct relations must be kept separate:**
- **Change origin / research provenance:** B is the existing unit that motivated the variant and helps explain the research question.
- **Actual mathematical/build dependency:** A and the expressly listed preceding roots (potentially a larger DAG of ancestors or parallel contributors) provide the foundations for B′.

There *may* be a proved mathematical link between B and B′, or none may be established or needed. A link `B → B′` is **not** implied by the fact that the researcher changed something about B. If B′ really consumes a result of B, declare and prove that dependency explicitly. If a more fundamental change requires fresh axioms or roots, document these as new, rather than pretending that the previous roots logically entail them.

A **mathematical branch** in the Construction DAG is not a GitHub **Git branch**. A Git branch is an implementation/provenance vehicle; a mathematical branch carries its own semantics, foundations, claims and proofs.

## 3. Two valid research modes — neither reduces to the other

**Branch-first exploratory construction:** introduce a mathematically grounded B′, build upon it, investigate what follows, and allow unanticipated structures. Impact on the existing B/C line, comparisons, isomorphisms and reconvergence are **optional research questions**, never default requirements.

**Change-impact study:** ask what a controlled alteration would affect in existing structures: downstream, upstream, lateral, direct, transitive, already recorded, newly discovered, or still unknown. A separate branch can serve as its test vehicle without editing the original.

These modes can be combined, but BOMA is **not merely impact analysis on a fixed construction**. When two routes are asserted to be equivalent or convergent, the assertion requires its own evidence; no branch is forced to return.

## 4. Constructional coherence back to roots

For each explored branch, make its root assumptions and mathematical ancestry auditably explicit:

1. Which existing unit prompted the change, and what is the actual branch point?
2. Which roots, predecessor units, parallel contributors, logical rules and *new* premises does the alternative really use?
3. Are the definitions well formed, and which consistency/adequacy obligations and proof claims are fulfilled versus open?
4. Can the proofs be checked and reproduced? Distinguish mathematical necessity from proof-implementation ancestry.
5. Was any relationship with the old branch established, refuted in a specified sense, not investigated or left open?

Root coherence means **traceable foundations and justified reasoning**, not identity with the original. Where assumptions are used, the exact conditional scope must remain visible; machine-checking conditional proofs does not itself establish absolute consistency or universal minimality.

## 5. Unknown outcomes, discovery and invention

A branch need not have an anticipated final object. Research may expose new structures, properties, dependencies, relationships or proof methods. Novelty **within BOMA** is not necessarily novelty **in the mathematical literature**; any claim of globally original discovery needs appropriate literature review and independent scrutiny.

Aiming at novelty never permits inventing results, hiding failures, silently adding axioms or weakening a frozen success criterion.

## 6. Failed and incomplete branches are research outputs

Retain provenance for successful, partial, stalled, contradictory, tool-failed and owner-paused research, not just accepted constructions. Document the question, change, assumptions, attempted proofs, counterexamples, exact evidence, unexpected findings and unresolved questions.

**Failure to finish a proof is not a proof of impossibility. A tool failure is not a mathematical counterexample. Passing CI is not sufficient to assert that all scientific or acceptance conditions passed.** Properly labeled incomplete and unsuccessful work can be valuable scientific and pedagogical knowledge.

## 7. Independent pedagogical value

BOMA can help teach *how mathematics is made*: specifying roots, varying definitions, pursuing alternative branches, understanding dependency, finding mistakes and learning from non-success. This value does not depend on proving a globally novel mathematical theorem.

## 8. What the existing N→Z→Q→R→C work means

The accepted number-system spine and its verified alternative routes constitute a **known-specification calibration/testbed**, not the conceptual perimeter of BOMA. Past tests of Dedekind vs Cauchy reals, P vs Q complex routes, branch reconvergence and dependency changes illustrate investigated capabilities, not a requirement that every future branch model a known structure.

**Do not infer current execution state from this identity reference.** Read `LAB/PDSA/STATUS.md`, current GitHub branch/PR evidence, and the latest binding owner decision. As of 2026-10-30, Draft PR #33 records a partially archived, non-PASS, non-closed ST2-EXP-016 study; it is **not** merged acceptance on `main`.

## 9. Scientific and governance integrity

- Preserve the original unit and construction history; do not silently mutate an existing branch when exploring an alternative.
- Separate change provenance, logical/build dependency, and any independently established comparison relation.
- No mandatory equivalence, superiority, comparison or reconvergence to the original.
- No hidden mathematical premises, untracked logical principles or laundering of historical proof roots.
- Distinguish verified mathematical claims, partial findings, implementation failures and lifecycle/administrative outcomes.
- Preserve negative, partial and failed evidence; distinguish inability to prove from proven impossibility.
- No automatic `SELECTS`, accepted export, architecture integration, merge or transition just because an alternative branch exists or an experiment passes.
- No global novelty claim without checking the literature.
- No autonomous action or new experiment is authorized by this identity document.

## 10. Human and AI onboarding contract

Always distinguish **project identity**, **current calibration testbed**, **accepted construction**, **independent exploratory branches**, **scientific outcome**, and **current operational authority**. Never define BOMA as “starting from known mathematics”; do not automatically make B′ depend on B; do not require branches to reconverge; do not promote partial Draft PR evidence to accepted `main` mathematics.

Read: `README.md` (entry point), `AGENTS.md` (AI instructions), `LAB/00_ARCHITECTURE/ARCHITECTURE.md` and `CONSTRUCTION_TOPOLOGY.md` (typed graph), `LAB/BOMA_PDSA_GOVERNANCE_AND_PDCA_LEGACY_CORRECTION_2026-08-18.md` (learning from all trials), `LAB/PDSA/STATUS.md` and the current 2026-10-29 interactive governance/owner decision (runtime authority).

**This is a conceptual owner clarification, not an automatic governance migration.** It does not alter frozen plans, canonical selections, acceptance contracts, mathematical sources, experiment states or PR-merge authority.
