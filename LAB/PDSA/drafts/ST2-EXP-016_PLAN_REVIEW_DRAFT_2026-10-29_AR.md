# ST2-EXP-016 — Independent Plan for Owner Review (Arabic DRAFT)

**Program:** `ST2-RP-001` — experiment 3/4  
**Document ID:** `ST2-EXP-016-PLAN-REVIEW-DRAFT-2026-10-29`  
**Status:** `DRAFT / OWNER_REVIEW / NOT_FROZEN / NO_DO / NOT_AUTHORIZED_TO_START`  
**Prepared:** 2026-10-29  
**Current-main reading baseline:** `3def8c26caf6cbf3ca03caed706fc02fe31f21a7`  
**Typed architectural origin:** `DEPENDENCY_EDGE / BOMA-C-R-DEP-001`  
**Owner authority:** owner explicitly requested preparation and presentation of an independent Plan; **not** freezing, experiment activation, implementation, or merge.  
**Current governance:** `LAB/PDSA/OWNER_DECISION_2026-10-29_INTERACTIVE_PDSA_MODE.md` and `LAB/PDSA/INTERACTIVE_PDSA_EXECUTION_GOVERNANCE_2026_10_29.md`.  
**Research frontier at drafting:** `ST2-EXP-015 CLOSED_PASS`; `ST2-EXP-016 NOT_STARTED / NO_FROZEN_PLAN`; `OWNER_REQUIRED`.

> **STOP: THIS IS AN UNFROZEN REVIEW DRAFT.** It is not the independent immutable Frozen Plan, has no machine twin, and grants no authority to run Lean, create scientific payloads, alter program state, or begin Do. If approved in a **later explicit owner instruction**, re-read the then-current main, reconcile any drift, prepare the separate canonical human Plan plus machine twin, and freeze them before the first Do. Do not silently promote this draft to a Frozen Plan.

## 1. الغاية البحثية والسؤال القابل للقياس
يدرس BOMA هنا أثر **تغيير افتراض واحد** عند حافة الاعتماد الرياضي `BOMA-C-R-DEP-001`:

**هل يمكن استعادة برهان معاني `C-CL-FIELD-001` و`C-CL-INTEGRATION-001` عند حذف حقل `orderTotal` من واجهة إنتاج المركب واستبداله بشرط جبري واحد عن عدم انحلال معيار مجموع المربعين، مع بقاء المطالب التسعة ومعنى البناء التربيعي ثابتاً؟**

تجيب التجربة عن سؤال *كفاية واجهة مضبوطة للبرهان المقترح*، لا عن ضرورة رياضية شاملة ولا عن أصغر مجموعة مسلمات ممكنة، ولا عن إزالة كل الاعتماد على الترتيب/المنطق الكلاسيكي من المصدر الحقيقي.

## 2. الأدلة الدقيقة التي تقوم عليها Plan
- **004, Gate E:** `LAB/PDSA/experiments/ST2-EXP-004_GATE_E_C_SENSITIVITY_001.md`; exact head `cf16d0e8f0285c69bc3ab5da7659efe50f4ac6`. حذف `orderTotal` وحده مع إبقاء الخمس عشرة الأخرى: 7 من 9 عائلات C نجت، بينما توقف الإغلاق الحالي لـ`C-CL-FIELD-001` و`C-CL-INTEGRATION-001`. التبعية العابرة تقع في `square_nonnegative → norm_nonzero → inverse witness`. عدم بقاء البرهان الحالي لا يثبت استحالة أي برهان بديل.
- **011:** `LAB/PDSA/experiments/ST2-EXP-011_FINAL_STUDY_ACT_001.md`; head `3a7510fb2fd71cfa7b75434a2ea265e654897ffe`. واجهة `C-COMPARE-BLOCK-001` منفصلة: `zero/one/neg/add/mul` وقوانين الإحداثيات؛ لا تعتمد مباشرة على الترتيب أو وجود المعكوس. العلاقة الكلية ليست دالة إلا مع `CoordinateExtractor` صريح؛ `C-CL-COMPARE-001` ضابط سلبي.
- **014:** `LAB/PDSA/experiments/ST2-EXP-014_FINAL_STUDY_ACT_001.md`; head `57fcc2797ae7670725d6c9ffd8659c9034a47d32`. إعادة إنتاج المعاني التسعة على `RCBOMA` مع Route P ثابتة؛ 7 من H6، والمقارنة من 011، والتكامل تغليف جديد؛ لا اعتماد تنفيذي أصلي على H5/Dedekind.
- **015:** `LAB/PDSA/experiments/ST2-EXP-015_FINAL_STUDY_ACT_001.md` و`ST2-EXP-015_TO_ST2-EXP-016_BOUNDARY_ASSESSMENT_001.json`؛ exact closed head `d91b32250f4cdc800f26b728e388902797bf5200`. Route Q مستقل فوق كوشي وإغلاق مربع D/Cauchy × P/Q، مع إبقاء `orderTotal` دون تغيير. تبعية Q الحالية تمر عبر `CauchyScalarCertificate.orderTotal` و`CauchyOrderTotal003.rcle_total`. المتطلبات العلمية لـ016 `MET` لكن الانتقال غير مفوض قبل أمر جديد.
- **البرنامج والـManifest:** `LAB/PDSA/RESEARCH_PROGRAM_ST2_RP_001_R_C_COMPOSITIONALITY_MINIMALITY.md` و`LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json`: الأصل `DEPENDENCY_EDGE`؛ العامل المحدد هو `PRODUCTION_ORDERTOTAL_TO_ONE_EXACT_FROZEN_NON_ORDER_ALGEBRAIC_NONDEGENERACY_CONDITION`. 016 شرط سابق لــ017.
- **السطح المقبول:** `LAB/00_ARCHITECTURE/C_R_DEPENDENCY_CONTRACT.md`: 16 خاصية *كافية* في اختبار 001، لا واجهة ثبتت أصغريتها؛ `ST2-EXP-004` لا يغيّر العقد المقبول.

## 3. العامل العلمي المتغير الوحيد — المقترح للمراجعة
**العامل:** استبدال إسقاط واجهة الإنتاج `orderTotal` **فقط** بافتراض جبري واحد `NormAnisotropy016`، مبني على نفس العمليات والحامل المجمّدين:

```text
NormAnisotropy016:
  forall a b : RBOMA,
    rAdd (rMulCandidate a a) (rMulCandidate b b) = rZero
      -> a = rZero AND b = rZero
```

هذا **تعريف مقترح لفرضية تجريبية واحدة**، وليس مبرهنة مثبتة هنا. صياغته المنطقية هي `a²+b²=0 ⇒ (a=0 ∧ b=0)`. لا نفترض شروطاً إضافية مثل `(-1)` غير مربع أو `¬∃x, x²=-1`: يمكن مناقشة تكافؤها لاحقاً أو إثباته كقضية مستقلة، لكن **لن** تُضاف إلى الشهادة المجمدة كافتراض ثانٍ.

**اختيار خط الأساس المقترح:** نفس الحامل `RBOMA` وعملياته، وطريقة C Route P المختبرة في Gate E للتجربة 004، بواجهة `RWithoutOrderTotalCertificate` ذات الخمس عشرة خاصية. هذا يعزل أثر العامل بالمقارنة المباشرة مع Gate E ولا يغيّر منتج المعاملات أو مسار المركب أثناء 016. المنتج `RCBOMA` وRoute Q ومربع 015 محفوظة كضوابط خارجية **غير متغيرة**، لا كعوامل ثانية. تقرير 016 يجب أن يفرق بين برهان مُجرّد من إسقاط `orderTotal` وبين أي إثبات خاص بالمنتج الفعلي `RBOMA` قد يستند إلى ترتيب مورّث قبل واجهة الإنتاج.

**ضوابط ثابتة لا يمكن التنازل عنها:**
1. الخمس عشرة خاصية الأخرى لواجهة إنتاج C في 004، دون إضافة/حذف/إعادة تعريف؛ والحامل `RBOMA`، و`rZero/rOne/rAdd/rMulCandidate/rNeg/rLE` نفسها.
2. معنى Route P: الحامل الثنائي، الإحداثيان، المولد `i`، العلاقة `i²=-1`، التضمين، المعيار `a²+b²`، المرافق، ووجود/وحدانية **شواهد** المعكوس دون مُختار شامل.
3. المعاني التسعة لمطالب C؛ `C-CL-FIELD-001` و`C-CL-INTEGRATION-001` هدفا الاستعادة، والسبعة الباقية ضوابط محفوظة.
4. العلاقة الوظيفية فقط بمستخرج `CoordinateExtractor` صريح؛ عدم تحويل مجرد وجود إحداثيات/معكوس إلى دالة اختيار.
5. `R-DP-001 SELECTS Dedekind`، `C-DP-001 SELECTS P`، `R-BLOCK-001`، `C-BLOCK-002 / CA-20`، `C-J-001`، جميع `SELECTS` وملفات الرياضيات المقبولة وFrozen Plans القديمة ومراجعها **دون تعديل**.
6. لا تغيير في تجارب 014/015، ولا تعميم إلى حقل مجرد `K` أو بناء `K[i]` (هذه مسألة 017)، ولا ترقية نتيجة البحث إلى قبول معماري.

## 4. ملاحظة منهجية حرجة: `normNonnegative`
في البرهان المعتمد لعاملي P وQ، سجل `CPairFieldCertificate` و`QNormalFieldCertificate` يحتوي على حقل مساعد `normNonnegative`. هذا **ليس بحد ذاته** عائلة مطالب C مستقلة في مصفوفة المطالب التسعة؛ لكن لا يجوز تجاهل أي التزام له دور دلالي في التصدير المقبول.

المقترح: بناء شهادة **بحثية جديدة** للبرهان الجبري تحفظ قوانين الحقل، وعدم التفاهة، ومعادلة حاصل ضرب المرافق، وعدم انعدام المعيار لعناصر المركب غير الصفرية، ووجود شاهد معكوس ووحدانيته، **من دون افتراض أن `normNonnegative` لا بد أن يظل حقلاً داخل بنية الشهادة البحثية نفسها**. على Gate A تدقيق ما إذا كان إسقاط `normNonnegative` يؤثر على أي معنى Claim مقبول أو واجهة معلنة؛ إذا كان ذلك صحيحاً، فهذا تعارض مع الضوابط يستلزم `OWNER_REQUIRED`، لا تخفيضاً صامتاً للهدف.

## 5. الفرضيات المعلنة مسبقاً
- **H1 — control fidelity:** تبقى شهادات السبعة الباقية من Gate E صحيحة بالواجهة ذات الخمس عشرة خاصية، دون الاعتماد على `NormAnisotropy016` أو `orderTotal` بشكل خفي.
- **H2 — algebraic norm bridge:** من الفرضية الجبرية الوحيدة ينتج `N(z)=0 → (z.re=0 ∧ z.im=0)`، ثم `z ≠ 0 → N(z) ≠ 0`، دون sign-split أو `square_nonnegative` أو فرضية جديدة.
- **H3 — field closure:** باستعمال `inverseExists` الموجود ضمن الخمس عشرة، يُبنى شاهد (w=N(z)^{-1}\bar z) وجودياً لكل (z\ne0)، وتُثبت قوانين الحقل ووحدانية الشاهد مع حفظ معنى `C-CL-FIELD-001`.
- **H4 — full nine-Claim integration:** يُنتج بحثياً معنى `C-CL-INTEGRATION-001` من شهادة الحقل الجديدة ومقارنة 011، مع تدقيق المعاني التسعة واحداً واحداً ومنع اختيار إحداثيات أو معكوس تلقائي.
- **H5 — proven dependency reduction, not exaggerated:** لا تحتوي *جذور البناء البحثي المجردة* أو تصريحاته على إسقاط `.orderTotal`، مع جرد دقيق لأي اعتماد مورث في إثبات `NormAnisotropy016` على `RBOMA`. لا ادعاء بإزالة جميع مبادئ الترتيب أو كلفة `Classical.choice` إلا بدليل منفصل.
- **H6 — provenance and governance:** كل الحدود والملفات المجمدة والأدلة وأثر المنطق وCI محفوظة؛ لا تغير رياضي غير العامل الوحيد ولا أثر قبول غير مصرح به.

## 6. بوابات التنفيذ المقترحة **بعد التجميد فقط**
- **Gate A — baseline and semantic inventory:** عند التفويض الفعلي يُقرأ `current main` من جديد، وتُقارن ملفات 004/011/014/015 والعقد المقبول وملفات الشهادة. تُسجّل مصفوفة المطالب التسعة، وجذور `C-CL-FIELD-001` و`C-CL-INTEGRATION-001`، وتصنيف `normNonnegative`. خطة بشرية مستقلة ونسخة آلة إن استلزم المدقق، مثبتتان في التزام **تجميد منفصل قبل Do**.
- **Gate B — control reproduction:** إعادة إثبات/تحديد الأصول السبعة على سطح 15 حقلاً بلا الفرضية الجديدة؛ فشل الضابط يوقف تفسير نتيجة 016 كأثر العامل الوحيد.
- **Gate C — purely algebraic norm:** إعداد مصدر بحثي مستقل للشهادة ذات 15+1 بدلاً من الإسقاط `orderTotal`، وبراهين `normZero→coordinatesZero` و`z≠0→norm≠0` و`z×conj(z)=embed(N(z))`. لا استخدام لـ`orderTotal` داخل البرهان التجريدي ولا افتراض موجب/ترتيب كلي ضمني.
- **Gate D — field + integration:** إنشاء جذور بحثية مستقلة لوجود/وحدانية شواهد المعكوس، وقوانين الحقل، والشهادة الجامعة، مع كامل Claim matrix ومعانيها؛ لا نقل مسار استدلال معتمد من مصدر R المقبول على سبيل الاختصار.
- **Gate E — source/declaration provenance:** مصدر/manifest أصليان للتجربة 016 فقط؛ قياس إغلاق التصريحات لكل جذر، و`#print axioms`، وفحص `sorry/admit/axiom/unsafe` والأسماء المستوردة وأي `Classical.choose` جديد؛ فصل تكلفة مثيل `RBOMA` عن البرهان المجرد. مراجعة `orderTotal` في المسار الجبري لا تكتفي ببحث نصي؛ يجب التحقق من التبعيات التصريحية الفعلية.
- **Gate F — controls and regression:** تشغيل Lean المثبت بحسب المرجع المقروء عند التجميد (التجارب السابقة تستعمل 4.32.1)، وفحوص البراهين المقبولة/004/011/014/015 والحوكمة التفاعلية، على نفس HEAD، مع حفظ run/job/attempt/artifact/SHA-256 وإثبات هوية شجرة الدمج؛ لا تشغيل محرك G8.
- **Gate G — Study / Act / lifecycle:** جدول `H1..H6` بأحكام `CONFIRMED / PARTIAL / REFUTED` أو `BLOCKED` مدعومة بالأدلة؛ تقرير أثر كل Claim والتبعية المنطقية والحل الجبري؛ حفظ محاولات الفشل. إغلاق الدورة وطلب دمج للمراجعة البشرية **دون دمج ذاتي**. لا يُحضّر أو يُجمّد 017 تلقائياً.

## 7. أحكام النجاح والفشل مسبقاً
**PASS علمي** فقط إذا أُثبتت H1–H6 على رأس تحقق واحد، مع استعادة `C-CL-FIELD-001` و`C-CL-INTEGRATION-001` وبقاء السبعة الأخرى كاملة المعنى، وغياب إسقاط `orderTotal` من البرهان التجريدي، وعدم إضافة أي فرضية أو مبدأ منطقي جديد في حدود المصدر التجريبي.

**INFORMATIVE FAIL** إذا وُجد دليل رياضي قابل لإعادة الإنتاج أن الشرط الواحد لا يكفي أو أن استعادة معنى مطلوب تستلزم عاملاً ثانياً أو تغييراً في الهدف، أو ثبتت نتيجة مضادة لفروض مجمدة. عدم إنجاز Goal أو فشل تنزيل أداة أو timeout لا يُعد برهان فشل رياضي؛ يصنّف `TECHNICAL_BLOCK` ويُحفظ.

**OWNER_REQUIRED** عند تغيير الشرط أو الحامل أو المنتج أو Route، أو إضافة اختيار شامل/فرضية منطقية، أو تغيير عقد قبول/خطة مجمدة/معايير PASS، أو الحاجة إلى تجربة وسيطة قبل 017. لا تضعف الفرضيات أو الفحوص لاحقاً للوصول إلى PASS.

## 8. أثر التجربة على ST2-EXP-017
نجاح 016 يمكن أن يبرر **التحضير منفصلاً** لاختبار تعميم البناء إلى `K[i]` بعد أن يكشف Study واجهة جبرية كافية لا مجرد واجهة تبدو مستقلة من حيث أسماء التصريحات. إذا ظلت الفرضيات الخمس عشرة تحتوي قيوداً ترتيبية، يجب الإبلاغ عن ذلك صراحة: لا يُسمح لــ017 باستنتاج تعميم إلى `K` غير مرتب إلا إذا صاغت Plan الخاصة بها فصل الفرضيات المطلوبة وأثبتته ضمن عاملها الواحد. وإذا فشل هذا الشرط الانتقالي، نعيد القرار إلى المالك قبل 017.

## 9. ما يحتاج إلى مراجعة المالك **قبل أي تجميد**
1. اعتماد أو رفض `NormAnisotropy016` بصفته **الفرضية البديلة الوحيدة**؛ أي اختيار آخر يتطلب تنقيح هذه المسودة قبل تجميدها.
2. اعتماد `RBOMA` وRoute P وواجهة 004 ذات 15 خاصية كضابط رئيسي، مع اعتبار كوشي وQ أدلة مقارنة خارجية محفوظة لا عوامل متغيرة.
3. تأكيد أن شهادة الحقل البحثية قد تختلف **في حقول البرهان المساعدة فقط** مع الحفاظ الصارم على معنى المطالب التسعة.
4. اعتماد بوابات H1–H6 ونطاق `OWNER_REQUIRED` إذا ظهرت حاجة رياضية إلى فرضية ثانية أو إلى تغيير هدف 016.
5. بعد موافقة منفصلة: إعادة قراءة الرأس الحقيقي، إنشاء Frozen Plan بشرية مستقلة ونسخة آلة متوافقة مع الضوابط، ثم **طلب إذن منفصل قبل Do** وفق التشغيل التفاعلي المعتمد.

**This document is a review artifact only; no Frozen Plan exists, no experiment is active, and no mathematical proof has been executed.**
