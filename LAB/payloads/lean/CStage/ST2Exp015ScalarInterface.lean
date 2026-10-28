/- Fixed Cauchy scalar certificate for 015. No changed scalar assumption.
Scalar proof provenance is recorded separately. -/
namespace BOMA.C.StageTwo.ScalarInterface015

open BOMA.Q.Quotient001
open BOMA.Q.Integration001
open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.StageTwo.CauchyOrderCore003
open BOMA.R.StageTwo.CauchyOrderTotal003
open BOMA.R.StageTwo.CauchyOrderedRing003
open BOMA.R.StageTwo.CauchyInverse003

/-- The alternative real zero and one are distinct by faithfulness of the
    constant accepted-rational embedding. -/
theorem rC_nontrivial : rCZero ≠ rCOne := by
  intro h
  have hq : rCOfQ qZero = rCOfQ qOne := h
  exact q_nontrivial (rCOfQ_injective hq)

/-- Right additive zero derived from commutativity and the verified left law. -/
theorem rCAdd_zero_right (x : RCBOMA) : rCAdd x rCZero = x := by
  rw [rCAdd_comm x rCZero, rCAdd_zero_left x]

/-- Negation fixes zero without any equality decision. -/
theorem rCNeg_zero : rCNeg rCZero = rCZero := by
  have h := rCAdd_neg_right rCZero
  rw [rCAdd_zero_left] at h
  exact h

/-- Additive inverse witnesses are unique in the alternative real additive
    group. -/
theorem rC_add_inverse_unique {x y : RCBOMA}
    (hxy : rCAdd x y = rCZero) : y = rCNeg x := by
  calc
    y = rCAdd rCZero y := (rCAdd_zero_left y).symm
    _ = rCAdd (rCAdd x (rCNeg x)) y := by rw [rCAdd_neg_right x]
    _ = rCAdd x (rCAdd (rCNeg x) y) := rCAdd_assoc x (rCNeg x) y
    _ = rCAdd x (rCAdd y (rCNeg x)) := by
      rw [rCAdd_comm (rCNeg x) y]
    _ = rCAdd (rCAdd x y) (rCNeg x) :=
      (rCAdd_assoc x y (rCNeg x)).symm
    _ = rCAdd rCZero (rCNeg x) := by rw [hxy]
    _ = rCNeg x := rCAdd_zero_left (rCNeg x)

/-- Alternative-real negation is involutive. -/
theorem rCNeg_involutive (x : RCBOMA) : rCNeg (rCNeg x) = x := by
  have hleft : rCAdd (rCNeg x) x = rCZero := by
    calc
      rCAdd (rCNeg x) x = rCAdd x (rCNeg x) := rCAdd_comm (rCNeg x) x
      _ = rCZero := rCAdd_neg_right x
  exact (rC_add_inverse_unique hleft).symm

/-- Right multiplicative zero derived from commutativity. -/
theorem rCMul_zero_right (x : RCBOMA) : rCMul x rCZero = rCZero := by
  rw [rCMul_comm x rCZero, rCMul_zero_left x]

/-- Right multiplicative one derived from commutativity. -/
theorem rCMul_one_right_local (x : RCBOMA) : rCMul x rCOne = x := by
  rw [rCMul_comm x rCOne, rCMul_one_left x]

/-- Multiplication by an additive inverse on the right negates the product. -/
theorem rCMul_neg_right (x y : RCBOMA) :
    rCMul x (rCNeg y) = rCNeg (rCMul x y) := by
  have hd := rCMul_add_right x y (rCNeg y)
  have hsum :
      rCAdd (rCMul x y) (rCMul x (rCNeg y)) = rCZero := by
    calc
      rCAdd (rCMul x y) (rCMul x (rCNeg y)) =
          rCMul x (rCAdd y (rCNeg y)) := hd.symm
      _ = rCMul x rCZero := by rw [rCAdd_neg_right y]
      _ = rCZero := rCMul_zero_right x
  exact rC_add_inverse_unique hsum

/-- Multiplication by an additive inverse on the left negates the product. -/
theorem rCMul_neg_left (x y : RCBOMA) :
    rCMul (rCNeg x) y = rCNeg (rCMul x y) := by
  calc
    rCMul (rCNeg x) y = rCMul y (rCNeg x) := rCMul_comm (rCNeg x) y
    _ = rCNeg (rCMul y x) := rCMul_neg_right y x
    _ = rCNeg (rCMul x y) := by rw [rCMul_comm y x]

/-- Squaring a negated alternative real gives the same square. -/
theorem rCMul_neg_neg_same (x : RCBOMA) :
    rCMul (rCNeg x) (rCNeg x) = rCMul x x := by
  calc
    rCMul (rCNeg x) (rCNeg x) = rCNeg (rCMul x (rCNeg x)) :=
      rCMul_neg_left x (rCNeg x)
    _ = rCNeg (rCNeg (rCMul x x)) := by rw [rCMul_neg_right x x]
    _ = rCMul x x := rCNeg_involutive _

structure CauchyScalarCertificate where
  orderTrans :
    ∀ {x y z : RCBOMA}, rCLE x y → rCLE y z → rCLE x z
  orderAntisymm :
    ∀ {x y : RCBOMA}, rCLE x y → rCLE y x → x = y
  orderTotal :
    ∀ x y : RCBOMA, rCLE x y ∨ rCLE y x
  nontrivial :
    rCZero ≠ rCOne
  addComm :
    ∀ x y : RCBOMA, rCAdd x y = rCAdd y x
  addAssoc :
    ∀ x y z : RCBOMA, rCAdd (rCAdd x y) z = rCAdd x (rCAdd y z)
  addZeroLeft :
    ∀ x : RCBOMA, rCAdd rCZero x = x
  addInverseRight :
    ∀ x : RCBOMA, rCAdd x (rCNeg x) = rCZero
  addTranslateOrderIff :
    ∀ x y c : RCBOMA, rCLE (rCAdd x c) (rCAdd y c) ↔ rCLE x y
  negOrderReversing :
    ∀ {x y : RCBOMA}, rCLE x y → rCLE (rCNeg y) (rCNeg x)
  mulComm :
    ∀ x y : RCBOMA, rCMul x y = rCMul y x
  mulAssoc :
    ∀ x y z : RCBOMA,
      rCMul (rCMul x y) z =
      rCMul x (rCMul y z)
  mulOneLeft :
    ∀ x : RCBOMA, rCMul rCOne x = x
  distribRight :
    ∀ x y z : RCBOMA,
      rCMul x (rCAdd y z) =
      rCAdd (rCMul x y) (rCMul x z)
  orderMulNonneg :
    ∀ {a b c : RCBOMA},
      rCLE a b → rCLE rCZero c →
      rCLE (rCMul a c) (rCMul b c)
  inverseExists :
    ∀ x : RCBOMA, x ≠ rCZero →
      ∃ y : RCBOMA, rCMul x y = rCOne


theorem translate_iff (x y c : RCBOMA) :
    rCLE (rCAdd x c) (rCAdd y c) ↔ rCLE x y := by
  constructor
  · intro h
    have ht := rcle_add_right h (rCNeg c)
    rw [rCAdd_assoc, rCAdd_assoc, rCAdd_neg_right, rCAdd_zero_right,
      rCAdd_zero_right] at ht
    exact ht
  · intro h
    exact rcle_add_right h c

theorem neg_reversing {x y : RCBOMA} (h : rCLE x y) :
    rCLE (rCNeg y) (rCNeg x) := by
  apply (translate_iff (rCNeg y) (rCNeg x) y).1
  rw [rCAdd_comm (rCNeg y) y, rCAdd_neg_right,
    rCAdd_comm (rCNeg x) y]
  have ht := rcle_add_right h (rCNeg x)
  rw [rCAdd_neg_right] at ht
  exact ht

theorem mul_monotone {a b c : RCBOMA}
    (hab : rCLE a b) (hc : rCLE rCZero c) :
    rCLE (rCMul a c) (rCMul b c) := by
  have hdiff := rcle_add_right hab (rCNeg a)
  rw [rCAdd_neg_right] at hdiff
  have hp := rcle_mul_nonneg hc hdiff
  rw [rCMul_add_right, rCMul_neg_right,
    rCMul_comm c b, rCMul_comm c a] at hp
  apply (translate_iff (rCMul a c) (rCMul b c) (rCNeg (rCMul a c))).1
  rw [rCAdd_neg_right]
  exact hp

theorem cauchyScalarCertificate : CauchyScalarCertificate where
  orderTrans := @rcle_trans
  orderAntisymm := @rcle_antisymm
  orderTotal := rcle_total
  nontrivial := rC_nontrivial
  addComm := rCAdd_comm
  addAssoc := rCAdd_assoc
  addZeroLeft := rCAdd_zero_left
  addInverseRight := rCAdd_neg_right
  addTranslateOrderIff := translate_iff
  negOrderReversing := @neg_reversing
  mulComm := rCMul_comm
  mulAssoc := rCMul_assoc
  mulOneLeft := rCMul_one_left
  distribRight := rCMul_add_right
  orderMulNonneg := @mul_monotone
  inverseExists := rC_inverse_exists

end BOMA.C.StageTwo.ScalarInterface015
