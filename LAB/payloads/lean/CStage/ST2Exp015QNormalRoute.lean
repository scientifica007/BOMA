/- Adapted proof pattern; see ST2-EXP-015_IMPLEMENTATION_PROVENANCE_001.md. -/
/- ST2-EXP-015: independent Route-Q-local quadratic normal-form operations.
This source reuses only Route Q's own NormalForm and fixed Cauchy real interface. -/
namespace BOMA.C.StageTwo.QNormalRoute015

open BOMA.R.StageTwo.CauchyQuotient003
open BOMA.R.StageTwo.CauchyAdditive003
open BOMA.R.StageTwo.CauchyMultiplicative003
open BOMA.R.StageTwo.CauchyOrderCore003
open BOMA.C.StageTwo.ScalarInterface015

open BOMA.C.StageTwo.ScalarConsequences015

/-- Q-local normalization carrier: never the selected Route P carrier. -/
abbrev NormalForm : Type := BOMA.C.StageTwo.QExpression015.NormalForm

theorem normal_ext {u v : NormalForm}
    (hre : u.re = v.re) (him : u.im = v.im) :
    u = v :=
  BOMA.C.StageTwo.QExpression015.normal_ext hre him

def zero : NormalForm := BOMA.C.StageTwo.QExpression015.nfReal rCZero
def one : NormalForm := BOMA.C.StageTwo.QExpression015.nfReal rCOne
def ofR (a : RCBOMA) : NormalForm := BOMA.C.StageTwo.QExpression015.nfReal a
def imag : NormalForm := BOMA.C.StageTwo.QExpression015.nfImag
def neg (u : NormalForm) : NormalForm := BOMA.C.StageTwo.QExpression015.nfNeg u
def add (u v : NormalForm) : NormalForm := BOMA.C.StageTwo.QExpression015.nfAdd u v
def mul (u v : NormalForm) : NormalForm := BOMA.C.StageTwo.QExpression015.nfMul u v

theorem add_zero_right_from_interface
    (C : CauchyScalarCertificate) (x : RCBOMA) :
    rCAdd x rCZero = x := by
  calc
    rCAdd x rCZero = rCAdd rCZero x := C.addComm x rCZero
    _ = x := C.addZeroLeft x

theorem mul_one_right_from_interface
    (C : CauchyScalarCertificate) (x : RCBOMA) :
    rCMul x rCOne = x := by
  calc
    rCMul x rCOne = rCMul rCOne x := C.mulComm x rCOne
    _ = x := C.mulOneLeft x

/-- P/Q-03: route-local real embedding is faithful. -/
theorem ofR_injective {a b : RCBOMA}
    (h : ofR a = ofR b) : a = b :=
  congrArg BOMA.C.StageTwo.QExpression015.NormalForm.re h

/-- Multiplication by the route-local generator extracts an imaginary coefficient. -/
theorem embed_mul_imag
    (C : CauchyScalarCertificate) (b : RCBOMA) :
    mul (ofR b) imag = ⟨rCZero, b⟩ := by
  apply normal_ext
  · change
      rCAdd (rCMul b rCZero)
        (rCNeg (rCMul rCZero rCOne)) = rCZero
    rw [mul_zero_right_from_interface C b,
        mul_zero_left_from_interface C rCOne,
        neg_zero_from_interface C,
        C.addZeroLeft rCZero]
  · change
      rCAdd (rCMul b rCOne)
        (rCMul rCZero rCZero) = b
    rw [mul_one_right_from_interface C b,
        mul_zero_left_from_interface C rCZero,
        add_zero_right_from_interface C b]

/-- Normal form of a real-plus-imaginary route-local expression. -/
theorem coordinate_expression
    (C : CauchyScalarCertificate) (a b : RCBOMA) :
    add (ofR a) (mul (ofR b) imag) = ⟨a, b⟩ := by
  rw [embed_mul_imag C b]
  apply normal_ext
  · exact add_zero_right_from_interface C a
  · exact C.addZeroLeft b

/-- P/Q-06: the distinguished generator squares to negative one. -/
theorem imag_squared
    (C : CauchyScalarCertificate) :
    mul imag imag = neg one := by
  apply normal_ext
  · change
      rCAdd (rCMul rCZero rCZero)
        (rCNeg (rCMul rCOne rCOne)) = rCNeg rCOne
    rw [mul_zero_left_from_interface C rCZero,
        C.mulOneLeft rCOne,
        C.addZeroLeft (rCNeg rCOne)]
  · change
      rCAdd (rCMul rCZero rCOne)
        (rCMul rCOne rCZero) = rCNeg rCZero
    rw [mul_zero_left_from_interface C rCOne,
        C.mulOneLeft rCZero,
        C.addZeroLeft rCZero,
        neg_zero_from_interface C]

/-- P/Q-07: every route-local candidate has a real/imaginary decomposition. -/
theorem decomposition
    (C : CauchyScalarCertificate) (z : NormalForm) :
    ∃ a b : RCBOMA, z = add (ofR a) (mul (ofR b) imag) := by
  refine ⟨z.re, z.im, ?_⟩
  rw [coordinate_expression C z.re z.im]

/-- P/Q-08: real/imaginary coordinates are unique at Route Q normal-form equality. -/
theorem decomposition_unique
    (C : CauchyScalarCertificate)
    {a b a' b' : RCBOMA}
    (h : add (ofR a) (mul (ofR b) imag) =
      add (ofR a') (mul (ofR b') imag)) :
    a = a' ∧ b = b' := by
  rw [coordinate_expression C a b,
      coordinate_expression C a' b'] at h
  exact ⟨congrArg BOMA.C.StageTwo.QExpression015.NormalForm.re h,
         congrArg BOMA.C.StageTwo.QExpression015.NormalForm.im h⟩

/-- P/Q-09: the imaginary generator is not in the embedded real line. -/
theorem imag_not_real
    (C : CauchyScalarCertificate) :
    ¬ ∃ a : RCBOMA, imag = ofR a := by
  rintro ⟨a, ha⟩
  have h : rCOne = rCZero := congrArg BOMA.C.StageTwo.QExpression015.NormalForm.im ha
  exact C.nontrivial h.symm

end BOMA.C.StageTwo.QNormalRoute015
