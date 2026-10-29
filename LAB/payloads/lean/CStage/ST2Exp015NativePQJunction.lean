/- ST2-EXP-015 Gate C: admitted only after independent native Q closure. -/
namespace BOMA.C.StageTwo.NativePQ015

open BOMA.C.StageTwo.ComparisonInterface011
open BOMA.C.StageTwo.ComparisonInterface011.NativeCauchy
open BOMA.C.StageTwo.QPresentation015
open BOMA.C.StageTwo.QQuotientField015
open BOMA.C.StageTwo.CauchyQuadratic003
open BOMA.C.StageTwo.CauchyNativeFullC014

/-- Both extractors are explicit representation data. -/
def pqIsomorphism : ConstructiveQuadraticIsomorphism h6Presentation qPresentation :=
  constructiveQuadraticIsomorphism h6Presentation qPresentation h6Extractor qExtractor

def qpIsomorphism : ConstructiveQuadraticIsomorphism qPresentation h6Presentation :=
  constructiveQuadraticIsomorphism qPresentation h6Presentation qExtractor h6Extractor

def pToQ (z : CCBOMA) : QBOMA := pqIsomorphism.forward z
def qToP (z : QBOMA) : CCBOMA := pqIsomorphism.backward z

theorem pToQ_formula (z : CCBOMA) : pToQ z = qCoord z.re z.im := rfl
theorem qToP_formula (z : QBOMA) : qToP z = ⟨qRe z, qIm z⟩ := rfl

theorem forward_inverse_witness {x y : CCBOMA} (h : ccMul x y = ccOne) :
    qMul (pToQ x) (pToQ y) = qOne := by
  calc
    qMul (pToQ x) (pToQ y) = pToQ (ccMul x y) :=
      (pqIsomorphism.preserveMul x y).symm
    _ = pToQ ccOne := congrArg pToQ h
    _ = qOne := pqIsomorphism.preserveOne

theorem reverse_inverse_witness {x y : QBOMA} (h : qMul x y = qOne) :
    ccMul (qToP x) (qToP y) = ccOne := by
  calc
    ccMul (qToP x) (qToP y) = qToP (qMul x y) :=
      (qpIsomorphism.preserveMul x y).symm
    _ = qToP qOne := congrArg qToP h
    _ = ccOne := qpIsomorphism.preserveOne

structure NativePQJunctionCertificate where
  independentQ : NativeQFullCertificate
  fixedP : CauchyNativeFullCCertificate
  comparison : QuadraticComparisonCertificate h6Presentation qPresentation
  forward : ConstructiveQuadraticIsomorphism h6Presentation qPresentation
  reverse : ConstructiveQuadraticIsomorphism qPresentation h6Presentation
  forwardInverseWitness : ∀ {x y : CCBOMA}, ccMul x y = ccOne →
    qMul (pToQ x) (pToQ y) = qOne
  reverseInverseWitness : ∀ {x y : QBOMA}, qMul x y = qOne →
    ccMul (qToP x) (qToP y) = ccOne

def nativePQJunctionCertificate : NativePQJunctionCertificate where
  independentQ := nativeQFullCertificate
  fixedP := cauchyNativeFullCCertificate
  comparison := quadraticComparison h6Presentation qPresentation
  forward := pqIsomorphism
  reverse := qpIsomorphism
  forwardInverseWitness := @forward_inverse_witness
  reverseInverseWitness := @reverse_inverse_witness

end BOMA.C.StageTwo.NativePQ015
