/- ST2-EXP-015: independent Q comparison presentation and full Claim meanings. -/
namespace BOMA.C.StageTwo.QPresentation015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.C.StageTwo.ScalarInterface015
open BOMA.C.StageTwo.QQuotientField015
open BOMA.C.StageTwo.ComparisonInterface011

def scalarOps : ScalarOps where
  carrier := RCBOMA
  zero := rCZero
  one := rCOne
  neg := rCNeg
  add := rCAdd
  mul := rCMul

def qPresentation : QuadraticPresentation scalarOps where
  carrier := QBOMA
  zero := qZero
  one := qOne
  neg := qNeg
  add := qAdd
  mul := qMul
  ofScalar := qOfR
  imag := qI
  coord := qCoord
  coordinateGeneration := q_generation cauchyScalarCertificate
  coordinateUnique := @q_coordinate_unique cauchyScalarCertificate
  coordinateZero := q_coordinate_zero cauchyScalarCertificate
  coordinateOne := q_coordinate_one cauchyScalarCertificate
  coordinateReal := q_coordinate_real cauchyScalarCertificate
  coordinateImag := q_coordinate_imag cauchyScalarCertificate
  coordinateNeg := q_coordinate_neg cauchyScalarCertificate
  coordinateAdd := q_coordinate_add cauchyScalarCertificate
  coordinateMul := q_coordinate_mul cauchyScalarCertificate

def qExtractor : CoordinateExtractor qPresentation where
  re := qRe
  im := qIm
  sound := q_extract_sound cauchyScalarCertificate

theorem qNativeComparison (B : QuadraticPresentation scalarOps) :
    QuadraticComparisonCertificate qPresentation B :=
  quadraticComparison qPresentation B

def qNativeFunctionalComparison (B : QuadraticPresentation scalarOps)
    (E : CoordinateExtractor B) :
    ConstructiveQuadraticIsomorphism qPresentation B :=
  constructiveQuadraticIsomorphism qPresentation B qExtractor E

/-- Nine-family research meaning, with field and comparison roots kept distinct. -/
structure NativeQFullCertificate where
  field : QFieldCertificate
  comparison : ∀ B : QuadraticPresentation scalarOps,
    QuadraticComparisonCertificate qPresentation B
  functionalComparison : ∀ B : QuadraticPresentation scalarOps,
    CoordinateExtractor B → ConstructiveQuadraticIsomorphism qPresentation B

def nativeQFullCertificate : NativeQFullCertificate where
  field := qFieldCertificateFromCauchyR
  comparison := qNativeComparison
  functionalComparison := qNativeFunctionalComparison

end BOMA.C.StageTwo.QPresentation015
