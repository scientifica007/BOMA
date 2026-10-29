/- Adapted proof pattern; see ST2-EXP-015_IMPLEMENTATION_PROVENANCE_001.md. -/
/- C-stage fixed-Cauchy-R interface sufficiency probe.

Purpose:
  derive the order facts needed by likely C constructions from an abstract
  CauchyScalarCertificate first, then instantiate the result with the
  fixed Cauchy R certificate. The abstract proof does not unfold LowerCut,
  CutEquiv, quotient representatives, or the selected earlier scalar
  multiplication/inverse implementations.

This file does not construct a complex carrier and does not select C-DP-001.
-/
namespace BOMA.C.StageTwo.ScalarConsequences015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.StageTwo.CauchyOrderCore003
open BOMA.C.StageTwo.ScalarInterface015


/-- Zero is fixed by negation, derived only from the fixed scalar additive interface. -/
theorem neg_zero_from_interface
    (C : CauchyScalarCertificate) :
    rCNeg rCZero = rCZero := by
  calc
    rCNeg rCZero = rCAdd rCZero (rCNeg rCZero) :=
      (C.addZeroLeft (rCNeg rCZero)).symm
    _ = rCZero := C.addInverseRight rCZero

/-- Additive inverse witnesses are unique, derived from the fixed scalar additive laws. -/
theorem add_inverse_unique_from_interface
    (C : CauchyScalarCertificate)
    {x y : RCBOMA}
    (hxy : rCAdd x y = rCZero) :
    y = rCNeg x := by
  calc
    y = rCAdd rCZero y := (C.addZeroLeft y).symm
    _ = rCAdd (rCAdd x (rCNeg x)) y := by
      rw [C.addInverseRight x]
    _ = rCAdd x (rCAdd (rCNeg x) y) :=
      C.addAssoc x (rCNeg x) y
    _ = rCAdd x (rCAdd y (rCNeg x)) := by
      rw [C.addComm (rCNeg x) y]
    _ = rCAdd (rCAdd x y) (rCNeg x) :=
      (C.addAssoc x y (rCNeg x)).symm
    _ = rCAdd rCZero (rCNeg x) := by rw [hxy]
    _ = rCNeg x := C.addZeroLeft (rCNeg x)

/-- Negation is involutive, derived from fixed scalar additive commutativity and inverse uniqueness. -/
theorem neg_involutive_from_interface
    (C : CauchyScalarCertificate)
    (x : RCBOMA) :
    rCNeg (rCNeg x) = x := by
  have hleft : rCAdd (rCNeg x) x = rCZero := by
    calc
      rCAdd (rCNeg x) x = rCAdd x (rCNeg x) := C.addComm (rCNeg x) x
      _ = rCZero := C.addInverseRight x
  exact (add_inverse_unique_from_interface C hleft).symm

/-- Right zero-annihilation follows from distributivity and the fixed scalar additive group laws. -/
theorem mul_zero_right_from_interface
    (C : CauchyScalarCertificate)
    (x : RCBOMA) :
    rCMul x rCZero = rCZero := by
  let p : RCBOMA := rCMul x rCZero
  have hdist := C.distribRight x rCZero rCZero
  have h00 : rCAdd rCZero rCZero = rCZero := C.addZeroLeft rCZero
  have hp : p = rCAdd p p := by
    unfold p
    rw [h00] at hdist
    exact hdist
  have hnegleft : rCAdd (rCNeg p) p = rCZero := by
    calc
      rCAdd (rCNeg p) p = rCAdd p (rCNeg p) := C.addComm (rCNeg p) p
      _ = rCZero := C.addInverseRight p
  have hcancel := congrArg (fun t => rCAdd (rCNeg p) t) hp
  have hz_eq_p : rCZero = p := by
    calc
      rCZero = rCAdd (rCNeg p) p := hnegleft.symm
      _ = rCAdd (rCNeg p) (rCAdd p p) := hcancel
      _ = rCAdd (rCAdd (rCNeg p) p) p :=
        (C.addAssoc (rCNeg p) p p).symm
      _ = rCAdd rCZero p := by rw [hnegleft]
      _ = p := C.addZeroLeft p
  exact hz_eq_p.symm

/-- Left zero-annihilation follows from fixed scalar multiplication commutativity. -/
theorem mul_zero_left_from_interface
    (C : CauchyScalarCertificate)
    (x : RCBOMA) :
    rCMul rCZero x = rCZero := by
  calc
    rCMul rCZero x = rCMul x rCZero := C.mulComm rCZero x
    _ = rCZero := mul_zero_right_from_interface C x

/-- Multiplication by an additive inverse on the right negates the product. -/
theorem mul_neg_right_from_interface
    (C : CauchyScalarCertificate)
    (x y : RCBOMA) :
    rCMul x (rCNeg y) = rCNeg (rCMul x y) := by
  have hd := C.distribRight x y (rCNeg y)
  have hy0 : rCAdd y (rCNeg y) = rCZero := C.addInverseRight y
  have hsum :
      rCAdd (rCMul x y) (rCMul x (rCNeg y)) = rCZero := by
    calc
      rCAdd (rCMul x y) (rCMul x (rCNeg y)) =
          rCMul x (rCAdd y (rCNeg y)) := hd.symm
      _ = rCMul x rCZero := by rw [hy0]
      _ = rCZero := mul_zero_right_from_interface C x
  exact add_inverse_unique_from_interface C hsum

/-- Multiplication by an additive inverse on the left negates the product. -/
theorem mul_neg_left_from_interface
    (C : CauchyScalarCertificate)
    (x y : RCBOMA) :
    rCMul (rCNeg x) y = rCNeg (rCMul x y) := by
  calc
    rCMul (rCNeg x) y = rCMul y (rCNeg x) :=
      C.mulComm (rCNeg x) y
    _ = rCNeg (rCMul y x) := mul_neg_right_from_interface C y x
    _ = rCNeg (rCMul x y) := by rw [C.mulComm y x]

/-- Squaring a negated value gives the same square, using only fixed scalar field laws. -/
theorem mul_neg_neg_same_from_interface
    (C : CauchyScalarCertificate)
    (x : RCBOMA) :
    rCMul (rCNeg x) (rCNeg x) = rCMul x x := by
  calc
    rCMul (rCNeg x) (rCNeg x) =
        rCNeg (rCMul x (rCNeg x)) :=
      mul_neg_left_from_interface C x (rCNeg x)
    _ = rCNeg (rCNeg (rCMul x x)) := by
      rw [mul_neg_right_from_interface C x x]
    _ = rCMul x x := neg_involutive_from_interface C _

/-- C-RL-001 at the abstract fixed-Cauchy-R interface level: every square is nonnegative.

The proof branches only on total order supplied by the certificate. The
negative branch replaces x by -x and uses identities proved above from the
same abstract interface. -/
theorem square_nonnegative_of_interface
    (C : CauchyScalarCertificate)
    (x : RCBOMA) :
    rCLE rCZero (rCMul x x) := by
  rcases C.orderTotal rCZero x with h0x | hx0
  · have h := C.orderMulNonneg (a := rCZero) (b := x) (c := x) h0x h0x
    rw [mul_zero_left_from_interface C x] at h
    exact h
  · have h0nx0 := C.negOrderReversing hx0
    have h0nx : rCLE rCZero (rCNeg x) := by
      rw [neg_zero_from_interface C] at h0nx0
      exact h0nx0
    have h := C.orderMulNonneg
      (a := rCZero) (b := rCNeg x) (c := rCNeg x) h0nx h0nx
    rw [mul_zero_left_from_interface C (rCNeg x),
        mul_neg_neg_same_from_interface C x] at h
    exact h

/-- One is nonnegative as the square of one, at the abstract interface level. -/
theorem zero_le_one_of_interface
    (C : CauchyScalarCertificate) :
    rCLE rCZero rCOne := by
  have h := square_nonnegative_of_interface C rCOne
  rw [C.mulOneLeft rCOne] at h
  exact h

/-- C-RL-002 at the abstract fixed-Cauchy-R interface level: -1 is not a square. -/
theorem minus_one_not_square_of_interface
    (C : CauchyScalarCertificate) :
    ¬ ∃ x : RCBOMA, rCMul x x = rCNeg rCOne := by
  rintro ⟨x, hx⟩
  have hsq : rCLE rCZero (rCNeg rCOne) := by
    have h := square_nonnegative_of_interface C x
    rw [hx] at h
    exact h
  have h10raw := C.negOrderReversing hsq
  have h10 : rCLE rCOne rCZero := by
    rw [neg_involutive_from_interface C rCOne,
        neg_zero_from_interface C] at h10raw
    exact h10raw
  have h01 : rCLE rCZero rCOne := zero_le_one_of_interface C
  have hEq : rCZero = rCOne := C.orderAntisymm h01 h10
  exact C.nontrivial hEq

/-- C-RL-001 instantiated on the fixed Cauchy R integration certificate. -/
theorem square_nonnegative_from_accepted_R (x : RCBOMA) :
    rCLE rCZero (rCMul x x) :=
  square_nonnegative_of_interface cauchyScalarCertificate x

/-- C-RL-002 instantiated on the fixed Cauchy R integration certificate.

This is the route-neutral C boundary fact needed to prevent a future
imaginary generator from collapsing into the embedded real line. -/
theorem minus_one_not_square_from_accepted_R :
    ¬ ∃ x : RCBOMA, rCMul x x = rCNeg rCOne :=
  minus_one_not_square_of_interface cauchyScalarCertificate

end BOMA.C.StageTwo.ScalarConsequences015
