/- ST2-EXP-016 owner-authorized SUPPLEMENTAL Do:
   EXTERNAL semantic adapter between experimental 15+1 Route P and accepted
   C carrier/certificate vocabulary. Not an ingredient of abstract 016 roots.
   Selected field/integration producers are NOT proof oracles here.
   Accepted real-order evidence may enter only the external normNonnegative
   auxiliary, and must be classified separately. No acceptance promotion. -/
namespace BOMA.C.StageTwo.NormAnisotropy016.AcceptedBridge
open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindNegationCandidate001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.R.StageIntegration002
open BOMA.C.RInterfaceNoSquareProbe001
open BOMA.C.PairCore001
open BOMA.C.PairNormInverse001
open BOMA.C.QuadraticComparison001
open BOMA.C.StageTwo.TotalOrderRegime004.WithoutOrderTotal
open BOMA.C.StageTwo.NormAnisotropy016

/-- Explicit isomorphism of the two distinct Lean pair RECORD carriers.
    This is a representation map, not definitional equality of their types. -/
def toSelected016 (z : Pair004) : CBOMA := ⟨z.re, z.im⟩
def fromSelected016 (z : CBOMA) : Pair004 := ⟨z.re, z.im⟩

theorem toFrom016 (z : CBOMA) : toSelected016 (fromSelected016 z) = z := by
  cases z
  rfl
theorem fromTo016 (z : Pair004) : fromSelected016 (toSelected016 z) = z := by
  cases z
  rfl

theorem toZero016 : toSelected016 zero004 = cZero := rfl
theorem toOne016 : toSelected016 one004 = cOne := rfl
theorem toImag016 : toSelected016 imag004 = cI := rfl
theorem toReal016 (a : RBOMA) : toSelected016 (ofR004 a) = cOfR a := rfl
theorem toNeg016 (z : Pair004) :
    toSelected016 (neg004 z) = cNeg (toSelected016 z) := rfl
theorem toAdd016 (z w : Pair004) :
    toSelected016 (add004 z w) = cAdd (toSelected016 z) (toSelected016 w) := rfl
theorem toMul016 (z w : Pair004) :
    toSelected016 (mul004 z w) = cMul (toSelected016 z) (toSelected016 w) := rfl
theorem toConj016 (z : Pair004) :
    toSelected016 (conj016 z) = cConj (toSelected016 z) := rfl
theorem toNorm016 (z : Pair004) :
    norm016 z = cNorm (toSelected016 z) := rfl

/-- The frozen 15+1 research factor supplies accepted-carrier inverse
    existence WITHOUT using the selected C inverse proof as oracle. -/
theorem selectedInverseExists016 (C : RNormAnisotropyCertificate016)
    (z : CBOMA) (hz : z ≠ cZero) :
    ∃ w : CBOMA, cMul z w = cOne := by
  have hz004 : fromSelected016 z ≠ zero004 := by
    intro heq
    apply hz
    calc
      z = toSelected016 (fromSelected016 z) := (toFrom016 z).symm
      _ = toSelected016 zero004 := congrArg toSelected016 heq
      _ = cZero := toZero016
  rcases (fieldCertificate016 C).inverseExists (fromSelected016 z) hz004
    with ⟨w, hw⟩
  refine ⟨toSelected016 w, ?_⟩
  have hw' := congrArg toSelected016 hw
  simpa only [toMul016, toOne016, toFrom016] using hw'

theorem selectedNormNonzero016 (C : RNormAnisotropyCertificate016)
    (z : CBOMA) (hz : z ≠ cZero) : cNorm z ≠ rZero := by
  have hz004 : fromSelected016 z ≠ zero004 := by
    intro heq
    apply hz
    calc
      z = toSelected016 (fromSelected016 z) := (toFrom016 z).symm
      _ = toSelected016 zero004 := congrArg toSelected016 heq
      _ = cZero := toZero016
  have hn := (fieldCertificate016 C).normNonzero (fromSelected016 z) hz004
  simpa only [toNorm016, toFrom016] using hn

theorem selectedConjugateProduct016 (C : RNormAnisotropyCertificate016)
    (z : CBOMA) : cMul z (cConj z) = cOfR (cNorm z) := by
  have hh := congrArg toSelected016
    ((fieldCertificate016 C).conjProduct (fromSelected016 z))
  simpa only [toMul016, toConj016, toReal016, toFrom016, toNorm016] using hh

theorem selectedInverseUnique016 (C : RNormAnisotropyCertificate016)
    {z w v : CBOMA}
    (hzw : cMul z w = cOne) (hzv : cMul z v = cOne) : w = v := by
  have h1 : mul004 (fromSelected016 z) (fromSelected016 w) = one004 := by
    have hh := congrArg fromSelected016 hzw
    simpa [fromSelected016, mul004, cMul, cOne,
      BOMA.C.RoutePairProbe001.mul, BOMA.C.RoutePairProbe001.one] using hh
  have h2 : mul004 (fromSelected016 z) (fromSelected016 v) = one004 := by
    have hh := congrArg fromSelected016 hzv
    simpa [fromSelected016, mul004, cMul, cOne,
      BOMA.C.RoutePairProbe001.mul, BOMA.C.RoutePairProbe001.one] using hh
  have heq := (fieldCertificate016 C).inverseUnique h1 h2
  have ht := congrArg toSelected016 heq
  simpa only [toFrom016] using ht

/-- Auxiliary historical nonnegative norm is proved from the *accepted R*
    ordered interface only. It is neither an extra 016 algebraic assumption
    nor a consequence asserted of abstract NormAnisotropy016. -/
theorem selectedNormNonnegativeExternal016
    (R : RStageIntegrationCertificate) (z : CBOMA) :
    rLE rZero (cNorm z) := by
  have h0re := square_nonnegative_of_interface R z.re
  have h0im := square_nonnegative_of_interface R z.im
  have h :=
    (R.addTranslateOrderIff rZero
      (rMulCandidate z.im z.im) (rMulCandidate z.re z.re)).2 h0im
  rw [R.addZeroLeft (rMulCandidate z.re z.re),
      R.addComm (rMulCandidate z.im z.im) (rMulCandidate z.re z.re)] at h
  exact R.orderTrans h0re h

/-- Accepted *type* of field certificate, filled with 016 inverse/field
    witness and the fixed historical ring core and external R auxiliary.
    It does NOT import cPairFieldCertificate or its accepted instantiation. -/
def selectedFieldCompatibility016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) : CPairFieldCertificate where
  ring := cPairRingCoreCertificate R
  normNonnegative := selectedNormNonnegativeExternal016 R
  normNonzero := selectedNormNonzero016 C
  conjugateProduct := selectedConjugateProduct016 C
  inverseExists := selectedInverseExists016 C
  inverseUnique := @selectedInverseUnique016 C

/-- Research field-strength package presented at the EXACT accepted
    QuadraticFieldPresentation signature. No selected C field producer
    or selected inverse proof is used to fill any field here. -/
def researchAcceptedPresentation016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) : QuadraticFieldPresentation R where
  carrier := Pair004
  zero := zero004
  one := one004
  neg := neg004
  add := add004
  mul := mul004
  ofR := ofR004
  imag := imag004
  coord := fun a b => ⟨a, b⟩
  nontrivial := (nineClaimMeaningCertificate016 C).pairNontrivial
  addComm := (fieldCertificate016 C).addComm
  addAssoc := (fieldCertificate016 C).addAssoc
  addZeroLeft := (fieldCertificate016 C).addZero
  addInverseRight := (fieldCertificate016 C).addInverse
  mulComm := (fieldCertificate016 C).mulComm
  mulAssoc := (fieldCertificate016 C).mulAssoc
  mulOneLeft := (fieldCertificate016 C).mulOne
  distribRight := (fieldCertificate016 C).distrib
  inverseExists := (fieldCertificate016 C).inverseExists
  inverseUnique := (fieldCertificate016 C).inverseUnique
  embeddingInjective := (nineClaimMeaningCertificate016 C).embeddingInjective
  embeddingZero := (nineClaimMeaningCertificate016 C).embeddingZero
  embeddingOne := (nineClaimMeaningCertificate016 C).embeddingOne
  embeddingNeg := (nineClaimMeaningCertificate016 C).embeddingNeg
  embeddingAdd := (nineClaimMeaningCertificate016 C).embeddingAdd
  embeddingMul := (nineClaimMeaningCertificate016 C).embeddingMul
  imagSquared := (nineClaimMeaningCertificate016 C).generatorSquared
  coordinateExpression := fun a b => (coordinate_expression004 C.scalar a b).symm
  coordinateGeneration := fun z => ⟨z.re,z.im,by cases z; rfl⟩
  coordinateUnique := by
    intro a b c d hh
    exact ⟨congrArg Pair004.re hh, congrArg Pair004.im hh⟩
  coordinateZero := rfl
  coordinateOne := rfl
  coordinateReal := fun _ => rfl
  coordinateImag := rfl
  coordinateNeg := fun _ _ => rfl
  coordinateAdd := fun _ _ _ _ => rfl
  coordinateMul := fun _ _ _ _ => rfl

/-- Same accepted comparison *type* with genuinely 016-derived field
    presentation as its source, and no inferred global selector. -/
def researchExactComparison016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate)
    (B : QuadraticFieldPresentation R) :
    QuadraticComparisonCertificate (researchAcceptedPresentation016 C R) B :=
  quadraticComparison (researchAcceptedPresentation016 C R) B

def researchExactExtractor016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) :
    CoordinateExtractor (researchAcceptedPresentation016 C R) where
  re := fun z => z.re
  im := fun z => z.im
  sound := fun z => by cases z; rfl

def researchExactFunctionalComparison016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate)
    (B : QuadraticFieldPresentation R) (E : CoordinateExtractor B) :
    ConstructiveQuadraticIsomorphism (researchAcceptedPresentation016 C R) B :=
  constructiveQuadraticIsomorphism
    (researchAcceptedPresentation016 C R) B
    (researchExactExtractor016 C R) E

/-- Exact accepted selected-presentation comparison **as comparison target**.
    This proves a coordinate-field map, not a new accepted Junction/V5. -/
def compareResearchToSelected016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) :
    QuadraticComparisonCertificate
      (researchAcceptedPresentation016 C R) (selectedPresentation R) :=
  researchExactComparison016 C R (selectedPresentation R)

end BOMA.C.StageTwo.NormAnisotropy016.AcceptedBridge
