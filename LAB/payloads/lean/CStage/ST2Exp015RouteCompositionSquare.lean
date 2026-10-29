/- ST2-EXP-015 Gate D: external comparisons after both native gates pass.
The vertical maps use the fixed H5 scalar maps only in this external assembly. -/
namespace BOMA.C.StageTwo.RouteSquare015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindNegationCandidate001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.R.StageIntegration002
open BOMA.R.StageTwo.DedekindCauchyComparison003
open BOMA.C.PairCore001
open BOMA.C.StageTwo.CauchyQuadratic003
open BOMA.C.StageTwo.QQuotientField015
open BOMA.C.StageTwo.NativePQ015

abbrev DQ := BOMA.C.StageTwo.QQuotientField002.QBOMA
abbrev dqZero  : DQ := BOMA.C.StageTwo.QQuotientField002.qZero 
abbrev dqOne  : DQ := BOMA.C.StageTwo.QQuotientField002.qOne 
abbrev dqI  : DQ := BOMA.C.StageTwo.QQuotientField002.qI 
abbrev dqNeg (z : DQ) : DQ := BOMA.C.StageTwo.QQuotientField002.qNeg z
abbrev dqAdd (z w : DQ) : DQ := BOMA.C.StageTwo.QQuotientField002.qAdd z w
abbrev dqMul (z w : DQ) : DQ := BOMA.C.StageTwo.QQuotientField002.qMul z w
abbrev dqOfR (a : RBOMA) : DQ := BOMA.C.StageTwo.QQuotientField002.qOfR a
abbrev dqCoord (a b : RBOMA) : DQ := BOMA.C.StageTwo.QQuotientField002.qCoord a b
abbrev dqRe (z : DQ) : RBOMA := BOMA.C.StageTwo.QQuotientField002.qRe z
abbrev dqIm (z : DQ) : RBOMA := BOMA.C.StageTwo.QQuotientField002.qIm z

def dPQ := BOMA.C.StageTwo.PQJunction002.pqIsomorphism rStageIntegrationCertificate

def dQP := BOMA.C.QuadraticComparison001.constructiveQuadraticIsomorphism
  (BOMA.C.StageTwo.PQJunction002.quotientPresentation rStageIntegrationCertificate)
  (BOMA.C.QuadraticComparison001.selectedPresentation rStageIntegrationCertificate)
  (BOMA.C.StageTwo.PQJunction002.quotientExtractor rStageIntegrationCertificate)
  (BOMA.C.QuadraticComparison001.selectedExtractor rStageIntegrationCertificate)

def dPToQ (z : CBOMA) : DQ := dPQ.forward z
def dQToP (z : DQ) : CBOMA := dPQ.backward z

/-- The horizontal Dedekind maps are exactly the retained 002 maps. -/
theorem d_horizontal_forward_exact (z : CBOMA) :
    dPToQ z = BOMA.C.StageTwo.PQJunction002.pairToQuotient rStageIntegrationCertificate z := rfl

theorem d_horizontal_reverse_exact (z : DQ) :
    dQToP z = BOMA.C.StageTwo.PQJunction002.quotientToPair rStageIntegrationCertificate z := rfl

noncomputable def pCToD (z : CCBOMA) : CBOMA := ⟨cToD z.re, cToD z.im⟩
noncomputable def pDToC (z : CBOMA) : CCBOMA := ⟨dToC z.re, dToC z.im⟩

theorem nPQ_zero  : pToQ (ccZero) = qZero :=
  pqIsomorphism.preserveZero 

theorem nPQ_one  : pToQ (ccOne) = qOne :=
  pqIsomorphism.preserveOne 

theorem nPQ_imag  : pToQ (ccI) = qI :=
  pqIsomorphism.preserveImag 

theorem nPQ_real (a : RCBOMA) : pToQ (ccOfR a) = qOfR a :=
  pqIsomorphism.preserveReal a

theorem nPQ_neg (z : CCBOMA) : pToQ (ccNeg z) = qNeg (pToQ z) :=
  pqIsomorphism.preserveNeg z

theorem nPQ_add (z w : CCBOMA) : pToQ (ccAdd z w) = qAdd (pToQ z) (pToQ w) :=
  pqIsomorphism.preserveAdd z w

theorem nPQ_mul (z w : CCBOMA) : pToQ (ccMul z w) = qMul (pToQ z) (pToQ w) :=
  pqIsomorphism.preserveMul z w

theorem nQP_zero  : qToP (qZero) = ccZero :=
  qpIsomorphism.preserveZero 

theorem nQP_one  : qToP (qOne) = ccOne :=
  qpIsomorphism.preserveOne 

theorem nQP_imag  : qToP (qI) = ccI :=
  qpIsomorphism.preserveImag 

theorem nQP_real (a : RCBOMA) : qToP (qOfR a) = ccOfR a :=
  qpIsomorphism.preserveReal a

theorem nQP_neg (z : QBOMA) : qToP (qNeg z) = ccNeg (qToP z) :=
  qpIsomorphism.preserveNeg z

theorem nQP_add (z w : QBOMA) : qToP (qAdd z w) = ccAdd (qToP z) (qToP w) :=
  qpIsomorphism.preserveAdd z w

theorem nQP_mul (z w : QBOMA) : qToP (qMul z w) = ccMul (qToP z) (qToP w) :=
  qpIsomorphism.preserveMul z w

theorem dPQ_zero  : dPToQ (cZero) = dqZero :=
  dPQ.preserveZero 

theorem dPQ_one  : dPToQ (cOne) = dqOne :=
  dPQ.preserveOne 

theorem dPQ_imag  : dPToQ (cI) = dqI :=
  dPQ.preserveImag 

theorem dPQ_real (a : RBOMA) : dPToQ (cOfR a) = dqOfR a :=
  dPQ.preserveReal a

theorem dPQ_neg (z : CBOMA) : dPToQ (cNeg z) = dqNeg (dPToQ z) :=
  dPQ.preserveNeg z

theorem dPQ_add (z w : CBOMA) : dPToQ (cAdd z w) = dqAdd (dPToQ z) (dPToQ w) :=
  dPQ.preserveAdd z w

theorem dPQ_mul (z w : CBOMA) : dPToQ (cMul z w) = dqMul (dPToQ z) (dPToQ w) :=
  dPQ.preserveMul z w

theorem dQP_zero  : dQToP (dqZero) = cZero :=
  dQP.preserveZero 

theorem dQP_one  : dQToP (dqOne) = cOne :=
  dQP.preserveOne 

theorem dQP_imag  : dQToP (dqI) = cI :=
  dQP.preserveImag 

theorem dQP_real (a : RBOMA) : dQToP (dqOfR a) = cOfR a :=
  dQP.preserveReal a

theorem dQP_neg (z : DQ) : dQToP (dqNeg z) = cNeg (dQToP z) :=
  dQP.preserveNeg z

theorem dQP_add (z w : DQ) : dQToP (dqAdd z w) = cAdd (dQToP z) (dQToP w) :=
  dQP.preserveAdd z w

theorem dQP_mul (z w : DQ) : dQToP (dqMul z w) = cMul (dQToP z) (dQToP w) :=
  dQP.preserveMul z w

theorem native_inverse_left (z : CCBOMA) : qToP (pToQ z) = z :=
  pqIsomorphism.leftInverse z

theorem native_inverse_right (z : QBOMA) : pToQ (qToP z) = z :=
  pqIsomorphism.rightInverse z

theorem d_inverse_left (z : CBOMA) : dQToP (dPToQ z) = z := dPQ.leftInverse z
theorem d_inverse_right (z : DQ) : dPToQ (dQToP z) = z := dPQ.rightInverse z

theorem pCD_zero  : pCToD (ccZero) = cZero := by
  apply c_ext <;>
    simp only [pCToD, ccZero, cZero, BOMA.C.RoutePairProbe001.zero,
      cToD_zero]

theorem pCD_one  : pCToD (ccOne) = cOne := by
  apply c_ext <;>
    simp only [pCToD, ccOne, cOne, BOMA.C.RoutePairProbe001.one,
      cToD_zero, cToD_one]

theorem pCD_imag  : pCToD (ccI) = cI := by
  apply c_ext <;>
    simp only [pCToD, ccI, cI, BOMA.C.RoutePairProbe001.imag,
      cToD_zero, cToD_one]

theorem pCD_real (a : RCBOMA) : pCToD (ccOfR a) = cOfR (cToD a) := by
  apply c_ext <;>
    simp only [pCToD, ccOfR, cOfR, BOMA.C.RoutePairProbe001.ofR,
      cToD_zero]

theorem pCD_neg (z : CCBOMA) : pCToD (ccNeg z) = cNeg (pCToD z) := by
  apply c_ext <;>
    simp only [pCToD, ccNeg, cNeg, BOMA.C.RoutePairProbe001.neg,
      cToD_neg]

theorem pCD_add (z w : CCBOMA) : pCToD (ccAdd z w) = cAdd (pCToD z) (pCToD w) := by
  apply c_ext <;>
    simp only [pCToD, ccAdd, cAdd, BOMA.C.RoutePairProbe001.add,
      cToD_add]

theorem pCD_mul (z w : CCBOMA) : pCToD (ccMul z w) = cMul (pCToD z) (pCToD w) := by
  apply c_ext <;>
    simp only [pCToD, ccMul, cMul, BOMA.C.RoutePairProbe001.mul,
      cToD_neg, cToD_add, cToD_mul]

theorem pDC_zero  : pDToC (cZero) = ccZero := by
  apply cc_ext <;>
    simp only [pDToC, cZero, ccZero, BOMA.C.RoutePairProbe001.zero,
      dToC_zero]

theorem pDC_one  : pDToC (cOne) = ccOne := by
  apply cc_ext <;>
    simp only [pDToC, cOne, ccOne, BOMA.C.RoutePairProbe001.one,
      dToC_zero, dToC_one]

theorem pDC_imag  : pDToC (cI) = ccI := by
  apply cc_ext <;>
    simp only [pDToC, cI, ccI, BOMA.C.RoutePairProbe001.imag,
      dToC_zero, dToC_one]

theorem pDC_real (a : RBOMA) : pDToC (cOfR a) = ccOfR (dToC a) := by
  apply cc_ext <;>
    simp only [pDToC, cOfR, ccOfR, BOMA.C.RoutePairProbe001.ofR,
      dToC_zero]

theorem pDC_neg (z : CBOMA) : pDToC (cNeg z) = ccNeg (pDToC z) := by
  apply cc_ext <;>
    simp only [pDToC, cNeg, ccNeg, BOMA.C.RoutePairProbe001.neg,
      dToC_neg]

theorem pDC_add (z w : CBOMA) : pDToC (cAdd z w) = ccAdd (pDToC z) (pDToC w) := by
  apply cc_ext <;>
    simp only [pDToC, cAdd, ccAdd, BOMA.C.RoutePairProbe001.add,
      dToC_add]

theorem pDC_mul (z w : CBOMA) : pDToC (cMul z w) = ccMul (pDToC z) (pDToC w) := by
  apply cc_ext <;>
    simp only [pDToC, cMul, ccMul, BOMA.C.RoutePairProbe001.mul,
      dToC_neg, dToC_add, dToC_mul]

theorem p_inverse_left (z : CCBOMA) : pDToC (pCToD z) = z := by
  apply cc_ext <;> simp only [pDToC, pCToD, dToC_cToD]

theorem p_inverse_right (z : CBOMA) : pCToD (pDToC z) = z := by
  apply c_ext <;> simp only [pDToC, pCToD, cToD_dToC]

/-- Quotient vertical maps compare existing representations; they build neither field. -/
noncomputable def qCToD (z : QBOMA) : DQ := dPToQ (pCToD (qToP z))
noncomputable def qDToC (z : DQ) : QBOMA := pToQ (pDToC (dQToP z))

theorem qCD_coordinate_formula (z : QBOMA) :
    qCToD z = dqCoord (cToD (qRe z)) (cToD (qIm z)) := rfl

theorem qDC_coordinate_formula (z : DQ) :
    qDToC z = qCoord (dToC (dqRe z)) (dToC (dqIm z)) := rfl

theorem qCD_zero  : qCToD (qZero) = dqZero := by
  simp only [qCToD, nQP_zero, pCD_zero, dPQ_zero]

theorem qCD_one  : qCToD (qOne) = dqOne := by
  simp only [qCToD, nQP_one, pCD_one, dPQ_one]

theorem qCD_imag  : qCToD (qI) = dqI := by
  simp only [qCToD, nQP_imag, pCD_imag, dPQ_imag]

theorem qCD_real (a : RCBOMA) : qCToD (qOfR a) = dqOfR (cToD a) := by
  simp only [qCToD, nQP_real, pCD_real, dPQ_real]

theorem qCD_neg (z : QBOMA) : qCToD (qNeg z) = dqNeg (qCToD z) := by
  simp only [qCToD, nQP_neg, pCD_neg, dPQ_neg]

theorem qCD_add (z w : QBOMA) : qCToD (qAdd z w) = dqAdd (qCToD z) (qCToD w) := by
  simp only [qCToD, nQP_add, pCD_add, dPQ_add]

theorem qCD_mul (z w : QBOMA) : qCToD (qMul z w) = dqMul (qCToD z) (qCToD w) := by
  simp only [qCToD, nQP_mul, pCD_mul, dPQ_mul]

theorem qDC_zero  : qDToC (dqZero) = qZero := by
  simp only [qDToC, dQP_zero, pDC_zero, nPQ_zero]

theorem qDC_one  : qDToC (dqOne) = qOne := by
  simp only [qDToC, dQP_one, pDC_one, nPQ_one]

theorem qDC_imag  : qDToC (dqI) = qI := by
  simp only [qDToC, dQP_imag, pDC_imag, nPQ_imag]

theorem qDC_real (a : RBOMA) : qDToC (dqOfR a) = qOfR (dToC a) := by
  simp only [qDToC, dQP_real, pDC_real, nPQ_real]

theorem qDC_neg (z : DQ) : qDToC (dqNeg z) = qNeg (qDToC z) := by
  simp only [qDToC, dQP_neg, pDC_neg, nPQ_neg]

theorem qDC_add (z w : DQ) : qDToC (dqAdd z w) = qAdd (qDToC z) (qDToC w) := by
  simp only [qDToC, dQP_add, pDC_add, nPQ_add]

theorem qDC_mul (z w : DQ) : qDToC (dqMul z w) = qMul (qDToC z) (qDToC w) := by
  simp only [qDToC, dQP_mul, pDC_mul, nPQ_mul]

theorem q_inverse_left (z : QBOMA) : qDToC (qCToD z) = z := by
  simp only [qDToC, qCToD, d_inverse_left, p_inverse_left, native_inverse_right]

theorem q_inverse_right (z : DQ) : qCToD (qDToC z) = z := by
  simp only [qDToC, qCToD, native_inverse_left, p_inverse_right, d_inverse_right]

/-- Forward square: native P to Dedekind Q, for every native P element. -/
theorem square_forward (z : CCBOMA) : dPToQ (pCToD z) = qCToD (pToQ z) := by
  simp only [qCToD, native_inverse_left]

/-- Reverse square: Dedekind Q to native P, for every Dedekind Q element. -/
theorem square_reverse (z : DQ) : pDToC (dQToP z) = qToP (qDToC z) := by
  simp only [qDToC, native_inverse_left]

theorem pCD_inverse_witness {x y : CCBOMA}
    (h : ccMul x y = ccOne) : cMul (pCToD x) (pCToD y) = cOne := by
  have ht := congrArg pCToD h
  rw [pCD_mul, pCD_one] at ht
  exact ht

theorem pDC_inverse_witness {x y : CBOMA}
    (h : cMul x y = cOne) : ccMul (pDToC x) (pDToC y) = ccOne := by
  have ht := congrArg pDToC h
  rw [pDC_mul, pDC_one] at ht
  exact ht

theorem qCD_inverse_witness {x y : QBOMA}
    (h : qMul x y = qOne) : dqMul (qCToD x) (qCToD y) = dqOne := by
  have ht := congrArg qCToD h
  rw [qCD_mul, qCD_one] at ht
  exact ht

theorem qDC_inverse_witness {x y : DQ}
    (h : dqMul x y = dqOne) : qMul (qDToC x) (qDToC y) = qOne := by
  have ht := congrArg qDToC h
  rw [qDC_mul, qDC_one] at ht
  exact ht

structure RouteSquareCertificate where
  native : NativePQJunctionCertificate
  dedekind : BOMA.C.StageTwo.PQJunction002.QPairJunctionCertificate
  scalar : DedekindCauchyFieldIsomorphismCertificate
  horizontalForwardExact : ∀ z : CBOMA,
    dPToQ z = BOMA.C.StageTwo.PQJunction002.pairToQuotient rStageIntegrationCertificate z
  horizontalReverseExact : ∀ z : DQ,
    dQToP z = BOMA.C.StageTwo.PQJunction002.quotientToPair rStageIntegrationCertificate z
  pLeftInverse : ∀ z : CCBOMA, pDToC (pCToD z) = z
  pRightInverse : ∀ z : CBOMA, pCToD (pDToC z) = z
  qLeftInverse : ∀ z : QBOMA, qDToC (qCToD z) = z
  qRightInverse : ∀ z : DQ, qCToD (qDToC z) = z
  squareForward : ∀ z : CCBOMA, dPToQ (pCToD z) = qCToD (pToQ z)
  squareReverse : ∀ z : DQ, pDToC (dQToP z) = qToP (qDToC z)
  qForwardFormula : ∀ z : QBOMA, qCToD z = dqCoord (cToD (qRe z)) (cToD (qIm z))
  qReverseFormula : ∀ z : DQ, qDToC z = qCoord (dToC (dqRe z)) (dToC (dqIm z))
  pCD_zero : pCToD (ccZero) = cZero
  pCD_one : pCToD (ccOne) = cOne
  pCD_imag : pCToD (ccI) = cI
  pCD_real (a : RCBOMA) : pCToD (ccOfR a) = cOfR (cToD a)
  pCD_neg (z : CCBOMA) : pCToD (ccNeg z) = cNeg (pCToD z)
  pCD_add (z w : CCBOMA) : pCToD (ccAdd z w) = cAdd (pCToD z) (pCToD w)
  pCD_mul (z w : CCBOMA) : pCToD (ccMul z w) = cMul (pCToD z) (pCToD w)
  pCD_inverse_witness {x y : CCBOMA}
    (h : ccMul x y = ccOne) : cMul (pCToD x) (pCToD y) = cOne
  pDC_zero : pDToC (cZero) = ccZero
  pDC_one : pDToC (cOne) = ccOne
  pDC_imag : pDToC (cI) = ccI
  pDC_real (a : RBOMA) : pDToC (cOfR a) = ccOfR (dToC a)
  pDC_neg (z : CBOMA) : pDToC (cNeg z) = ccNeg (pDToC z)
  pDC_add (z w : CBOMA) : pDToC (cAdd z w) = ccAdd (pDToC z) (pDToC w)
  pDC_mul (z w : CBOMA) : pDToC (cMul z w) = ccMul (pDToC z) (pDToC w)
  pDC_inverse_witness {x y : CBOMA}
    (h : cMul x y = cOne) : ccMul (pDToC x) (pDToC y) = ccOne
  qCD_zero : qCToD (qZero) = dqZero
  qCD_one : qCToD (qOne) = dqOne
  qCD_imag : qCToD (qI) = dqI
  qCD_real (a : RCBOMA) : qCToD (qOfR a) = dqOfR (cToD a)
  qCD_neg (z : QBOMA) : qCToD (qNeg z) = dqNeg (qCToD z)
  qCD_add (z w : QBOMA) : qCToD (qAdd z w) = dqAdd (qCToD z) (qCToD w)
  qCD_mul (z w : QBOMA) : qCToD (qMul z w) = dqMul (qCToD z) (qCToD w)
  qCD_inverse_witness {x y : QBOMA}
    (h : qMul x y = qOne) : dqMul (qCToD x) (qCToD y) = dqOne
  qDC_zero : qDToC (dqZero) = qZero
  qDC_one : qDToC (dqOne) = qOne
  qDC_imag : qDToC (dqI) = qI
  qDC_real (a : RBOMA) : qDToC (dqOfR a) = qOfR (dToC a)
  qDC_neg (z : DQ) : qDToC (dqNeg z) = qNeg (qDToC z)
  qDC_add (z w : DQ) : qDToC (dqAdd z w) = qAdd (qDToC z) (qDToC w)
  qDC_mul (z w : DQ) : qDToC (dqMul z w) = qMul (qDToC z) (qDToC w)
  qDC_inverse_witness {x y : DQ}
    (h : dqMul x y = dqOne) : qMul (qDToC x) (qDToC y) = qOne

noncomputable def routeSquareCertificate : RouteSquareCertificate where
  native := nativePQJunctionCertificate
  dedekind := BOMA.C.StageTwo.PQJunction002.qPairJunctionCertificate
  scalar := dedekindCauchyFieldIsomorphismCertificate
  horizontalForwardExact := d_horizontal_forward_exact
  horizontalReverseExact := d_horizontal_reverse_exact
  pLeftInverse := p_inverse_left
  pRightInverse := p_inverse_right
  qLeftInverse := q_inverse_left
  qRightInverse := q_inverse_right
  squareForward := square_forward
  squareReverse := square_reverse
  qForwardFormula := qCD_coordinate_formula
  qReverseFormula := qDC_coordinate_formula
  pCD_zero := pCD_zero
  pCD_one := pCD_one
  pCD_imag := pCD_imag
  pCD_real := pCD_real
  pCD_neg := pCD_neg
  pCD_add := pCD_add
  pCD_mul := pCD_mul
  pCD_inverse_witness := @pCD_inverse_witness
  pDC_zero := pDC_zero
  pDC_one := pDC_one
  pDC_imag := pDC_imag
  pDC_real := pDC_real
  pDC_neg := pDC_neg
  pDC_add := pDC_add
  pDC_mul := pDC_mul
  pDC_inverse_witness := @pDC_inverse_witness
  qCD_zero := qCD_zero
  qCD_one := qCD_one
  qCD_imag := qCD_imag
  qCD_real := qCD_real
  qCD_neg := qCD_neg
  qCD_add := qCD_add
  qCD_mul := qCD_mul
  qCD_inverse_witness := @qCD_inverse_witness
  qDC_zero := qDC_zero
  qDC_one := qDC_one
  qDC_imag := qDC_imag
  qDC_real := qDC_real
  qDC_neg := qDC_neg
  qDC_add := qDC_add
  qDC_mul := qDC_mul
  qDC_inverse_witness := @qDC_inverse_witness

end BOMA.C.StageTwo.RouteSquare015
