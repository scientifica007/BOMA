/- ST2-EXP-016 external concrete-RBOMA audit only. This intentionally
   uses the historical ordered real producer to build the one new predicate.
   It is forbidden to use this result as an ingredient in the abstract 016
   field/integration root or claim global order independence. -/
namespace BOMA.C.StageTwo.ConcreteRBOMA016
open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.C.StageTwo.NarrowRInterface001
open BOMA.C.StageTwo.NarrowPairCore001
open BOMA.C.StageTwo.NarrowPairNormInverse001
open BOMA.C.StageTwo.TotalOrderRegime004.WithoutOrderTotal
open BOMA.C.StageTwo.NormAnisotropy016

/-- Fixed other fifteen fields, projected from the historical R certificate. -/
def concreteFifteen016 : RWithoutOrderTotalCertificate where
  orderTrans := narrowRFromAcceptedProducers.orderTrans
  orderAntisymm := narrowRFromAcceptedProducers.orderAntisymm
  nontrivial := narrowRFromAcceptedProducers.nontrivial
  addComm := narrowRFromAcceptedProducers.addComm
  addAssoc := narrowRFromAcceptedProducers.addAssoc
  addZeroLeft := narrowRFromAcceptedProducers.addZeroLeft
  addInverseRight := narrowRFromAcceptedProducers.addInverseRight
  addTranslateOrderIff := narrowRFromAcceptedProducers.addTranslateOrderIff
  negOrderReversing := narrowRFromAcceptedProducers.negOrderReversing
  mulComm := narrowRFromAcceptedProducers.mulComm
  mulAssoc := narrowRFromAcceptedProducers.mulAssoc
  mulOneLeft := narrowRFromAcceptedProducers.mulOneLeft
  distribRight := narrowRFromAcceptedProducers.distribRight
  orderMulNonneg := narrowRFromAcceptedProducers.orderMulNonneg
  inverseExists := narrowRFromAcceptedProducers.inverseExists

/-- The concrete RBOMA does satisfy the frozen single condition, using
    inherited 001 nonnegative-square proof. This is a non-abstract result. -/
theorem concreteNormAnisotropy016 (a b : RBOMA)
    (h : rAdd (rMulCandidate a a) (rMulCandidate b b) = rZero) :
    a = rZero ∧ b = rZero := by
  let z : CBOMA := ⟨a, b⟩
  have hnorm : cNorm z = rZero := by
    exact h
  have ha : rMulCandidate a a = rZero :=
    c_norm_zero_real_square narrowRFromAcceptedProducers z hnorm
  have hb : rMulCandidate b b = rZero :=
    c_norm_zero_imaginary_square narrowRFromAcceptedProducers z hnorm
  constructor
  · exact Classical.byContradiction
      (r_square_zero_not_nonzero narrowRFromAcceptedProducers ha)
  · exact Classical.byContradiction
      (r_square_zero_not_nonzero narrowRFromAcceptedProducers hb)

/-- An external concrete inhabitant; not an abstract Lean proof oracle. -/
def concreteAnisotropyCertificate016 : RNormAnisotropyCertificate016 where
  scalar := concreteFifteen016
  normAnisotropy := concreteNormAnisotropy016

/-- Consequence of the separately kernel-checked abstract 016 field proof. -/
def concreteFieldWitness016 : FieldCertificate016 concreteAnisotropyCertificate016 :=
  fieldCertificate016 concreteAnisotropyCertificate016

end BOMA.C.StageTwo.ConcreteRBOMA016
