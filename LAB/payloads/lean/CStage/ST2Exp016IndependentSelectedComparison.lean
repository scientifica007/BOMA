/- ST2-EXP-016: third owner-directed Do, external research only.
   Independently reconstruct selected CBOMA quadratic comparison using 016
   existential inverses; leave accepted C-J-001 and CA-20 unchanged. -/
namespace BOMA.C.StageTwo.NormAnisotropy016.IndependentSelected

open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindNegationCandidate001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.R.StageIntegration002
open BOMA.C.PairCore001
open BOMA.C.PairNormInverse001
open BOMA.C.QuadraticComparison001
open BOMA.C.StageTwo.NormAnisotropy016
open BOMA.C.StageTwo.NormAnisotropy016.AcceptedBridge

/-- Actual CBOMA carrier, 016 inverse proof, fixed accepted ring controls.
    The historical selectedPresentation and c_inverse_exists are NOT used. -/
def researchSelectedPresentation016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) : QuadraticFieldPresentation R where
  carrier := CBOMA
  zero := cZero
  one := cOne
  neg := cNeg
  add := cAdd
  mul := cMul
  ofR := cOfR
  imag := cI
  coord := fun a b => ⟨a, b⟩
  nontrivial := (cPairRingCoreCertificate R).nontrivial
  addComm := (cPairRingCoreCertificate R).addComm
  addAssoc := (cPairRingCoreCertificate R).addAssoc
  addZeroLeft := (cPairRingCoreCertificate R).addZeroLeft
  addInverseRight := (cPairRingCoreCertificate R).addInverseRight
  mulComm := (cPairRingCoreCertificate R).mulComm
  mulAssoc := (cPairRingCoreCertificate R).mulAssoc
  mulOneLeft := (cPairRingCoreCertificate R).mulOneLeft
  distribRight := (cPairRingCoreCertificate R).distribRight
  inverseExists := selectedInverseExists016 C
  inverseUnique := @selectedInverseUnique016 C
  embeddingInjective := (cPairRingCoreCertificate R).embeddingInjective
  embeddingZero := (cPairRingCoreCertificate R).embeddingZero
  embeddingOne := (cPairRingCoreCertificate R).embeddingOne
  embeddingNeg := (cPairRingCoreCertificate R).embeddingNeg
  embeddingAdd := (cPairRingCoreCertificate R).embeddingAdd
  embeddingMul := (cPairRingCoreCertificate R).embeddingMul
  imagSquared := (cPairRingCoreCertificate R).imagSquared
  coordinateExpression := by
    intro a b
    exact (BOMA.C.RoutePairProbe001.coordinate_expression R a b).symm
  coordinateGeneration := by
    intro z
    exact ⟨z.re, z.im, by cases z; rfl⟩
  coordinateUnique := by
    intro a b c d h
    exact ⟨congrArg BOMA.C.RoutePairProbe001.PairCandidate.re h,
      congrArg BOMA.C.RoutePairProbe001.PairCandidate.im h⟩
  coordinateZero := rfl
  coordinateOne := rfl
  coordinateReal := by intro a; rfl
  coordinateImag := rfl
  coordinateNeg := by intro a b; rfl
  coordinateAdd := by intro a b c d; rfl
  coordinateMul := by intro a b c d; rfl

/-- Explicit extraction only; no global Choice-based coordinate selector. -/
def researchSelectedExtractor016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) :
    CoordinateExtractor (researchSelectedPresentation016 C R) where
  re := fun z => z.re
  im := fun z => z.im
  sound := by intro z; cases z; rfl

/-- Original accepted comparison type, using the NEW 016-selected source. -/
theorem researchSelectedComparison016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate)
    (B : QuadraticFieldPresentation R) :
    QuadraticComparisonCertificate (researchSelectedPresentation016 C R) B :=
  quadraticComparison (researchSelectedPresentation016 C R) B

def researchSelectedFunctionalComparison016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate)
    (B : QuadraticFieldPresentation R) (E : CoordinateExtractor B) :
    ConstructiveQuadraticIsomorphism (researchSelectedPresentation016 C R) B :=
  constructiveQuadraticIsomorphism
    (researchSelectedPresentation016 C R) B
    (researchSelectedExtractor016 C R) E

/-- Research nine-Claim meaning interface. Not the accepted C-J-001 type:
    its accepted comparison target includes historical selectedPresentation. -/
structure ResearchSelectedNineClaims016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) where
  carrierExt : ∀ {z w : CBOMA},
    z.re = w.re → z.im = w.im → z = w
  embeddingInjective : ∀ {a b : RBOMA}, cOfR a = cOfR b → a = b
  embeddingZero : cOfR rZero = cZero
  embeddingOne : cOfR rOne = cOne
  embeddingNeg : ∀ a : RBOMA, cOfR (rNeg a) = cNeg (cOfR a)
  embeddingAdd : ∀ a b : RBOMA,
    cOfR (rAdd a b) = cAdd (cOfR a) (cOfR b)
  embeddingMul : ∀ a b : RBOMA,
    cOfR (rMulCandidate a b) = cMul (cOfR a) (cOfR b)
  field : CPairFieldCertificate
  generatorSquared : cMul cI cI = cNeg cOne
  realGeneration : ∀ z : CBOMA,
    ∃ a b : RBOMA, z = cAdd (cOfR a) (cMul (cOfR b) cI)
  coordinateUnique : ∀ {a b c d : RBOMA},
    cAdd (cOfR a) (cMul (cOfR b) cI) =
      cAdd (cOfR c) (cMul (cOfR d) cI) → a = c ∧ b = d
  imaginaryNotReal : ¬ ∃ a : RBOMA, cI = cOfR a
  comparison : ∀ (B : QuadraticFieldPresentation R),
    QuadraticComparisonCertificate (researchSelectedPresentation016 C R) B
  functionalComparison : ∀ (B : QuadraticFieldPresentation R),
    CoordinateExtractor B →
    ConstructiveQuadraticIsomorphism (researchSelectedPresentation016 C R) B

/-- Research ownership root: 016 field witness, fixed accepted ring controls,
    independent quadratic comparison, external real-order norm auxiliary. -/
def researchSelectedNineClaims016
    (C : RNormAnisotropyCertificate016)
    (R : RStageIntegrationCertificate) :
    ResearchSelectedNineClaims016 C R where
  carrierExt := @c_ext
  embeddingInjective := (cPairRingCoreCertificate R).embeddingInjective
  embeddingZero := (cPairRingCoreCertificate R).embeddingZero
  embeddingOne := (cPairRingCoreCertificate R).embeddingOne
  embeddingNeg := (cPairRingCoreCertificate R).embeddingNeg
  embeddingAdd := (cPairRingCoreCertificate R).embeddingAdd
  embeddingMul := (cPairRingCoreCertificate R).embeddingMul
  field := selectedFieldCompatibility016 C R
  generatorSquared := (cPairRingCoreCertificate R).imagSquared
  realGeneration := (cPairRingCoreCertificate R).generation
  coordinateUnique := (cPairRingCoreCertificate R).coordinateUnique
  imaginaryNotReal := (cPairRingCoreCertificate R).imagNotReal
  comparison := researchSelectedComparison016 C R
  functionalComparison := researchSelectedFunctionalComparison016 C R

def concreteIndependentSelectedNineClaims016 :
    ResearchSelectedNineClaims016
      BOMA.C.StageTwo.ConcreteRBOMA016.concreteAnisotropyCertificate016
      rStageIntegrationCertificate :=
  researchSelectedNineClaims016
    BOMA.C.StageTwo.ConcreteRBOMA016.concreteAnisotropyCertificate016
    rStageIntegrationCertificate

end BOMA.C.StageTwo.NormAnisotropy016.IndependentSelected
