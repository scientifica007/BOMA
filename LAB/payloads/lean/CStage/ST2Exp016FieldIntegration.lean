/- ST2-EXP-016 Gate D: independent research Route-P ring, norm and field.
    Proof patterns adapted from ST2-EXP-001 scalar algebraic lemmas and pair
    normalizer, but explicitly re-derived against ST2-EXP-004's exact
    FIFTEEN-property interface. NO selected field certificate is used.
    All previously verified 016 A/B/C roots remain separate and unchanged. -/
namespace BOMA.C.StageTwo.NormAnisotropy016
open BOMA.R.DedekindQuotient001
open BOMA.R.DedekindAddition001
open BOMA.R.DedekindNegationCandidate001
open BOMA.R.DedekindSignedMulCandidate001
open BOMA.C.StageTwo.TotalOrderRegime004.WithoutOrderTotal

theorem addInverseUnique016
    (C : RWithoutOrderTotalCertificate)
    {x y : RBOMA}
    (hxy : rAdd x y = rZero) :
    y = rNeg x := by
  calc
    y = rAdd rZero y := (C.addZeroLeft y).symm
    _ = rAdd (rAdd x (rNeg x)) y := by
      rw [C.addInverseRight x]
    _ = rAdd x (rAdd (rNeg x) y) :=
      C.addAssoc x (rNeg x) y
    _ = rAdd x (rAdd y (rNeg x)) := by
      rw [C.addComm (rNeg x) y]
    _ = rAdd (rAdd x y) (rNeg x) :=
      (C.addAssoc x y (rNeg x)).symm
    _ = rAdd rZero (rNeg x) := by rw [hxy]
    _ = rNeg x := C.addZeroLeft (rNeg x)

/-- Negation is involutive, derived from accepted additive commutativity and inverse uniqueness. -/
theorem negInvolutive016
    (C : RWithoutOrderTotalCertificate)
    (x : RBOMA) :
    rNeg (rNeg x) = x := by
  have hleft : rAdd (rNeg x) x = rZero := by
    calc
      rAdd (rNeg x) x = rAdd x (rNeg x) := C.addComm (rNeg x) x
      _ = rZero := C.addInverseRight x
  exact (addInverseUnique016 C hleft).symm

/-- Right zero-annihilation follows from distributivity and the accepted additive group laws. -/
theorem mulZeroRight016
    (C : RWithoutOrderTotalCertificate)
    (x : RBOMA) :
    rMulCandidate x rZero = rZero := by
  let p : RBOMA := rMulCandidate x rZero
  have hdist := C.distribRight x rZero rZero
  have h00 : rAdd rZero rZero = rZero := C.addZeroLeft rZero
  have hp : p = rAdd p p := by
    unfold p
    rw [h00] at hdist
    exact hdist
  have hnegleft : rAdd (rNeg p) p = rZero := by
    calc
      rAdd (rNeg p) p = rAdd p (rNeg p) := C.addComm (rNeg p) p
      _ = rZero := C.addInverseRight p
  have hcancel := congrArg (fun t => rAdd (rNeg p) t) hp
  have hz_eq_p : rZero = p := by
    calc
      rZero = rAdd (rNeg p) p := hnegleft.symm
      _ = rAdd (rNeg p) (rAdd p p) := hcancel
      _ = rAdd (rAdd (rNeg p) p) p :=
        (C.addAssoc (rNeg p) p p).symm
      _ = rAdd rZero p := by rw [hnegleft]
      _ = p := C.addZeroLeft p
  exact hz_eq_p.symm

/-- Left zero-annihilation follows from accepted multiplication commutativity. -/
theorem mulZeroLeft016
    (C : RWithoutOrderTotalCertificate)
    (x : RBOMA) :
    rMulCandidate rZero x = rZero := by
  calc
    rMulCandidate rZero x = rMulCandidate x rZero := C.mulComm rZero x
    _ = rZero := mulZeroRight016 C x

/-- Multiplication by an additive inverse on the right negates the product. -/
theorem mulNegRight016
    (C : RWithoutOrderTotalCertificate)
    (x y : RBOMA) :
    rMulCandidate x (rNeg y) = rNeg (rMulCandidate x y) := by
  have hd := C.distribRight x y (rNeg y)
  have hy0 : rAdd y (rNeg y) = rZero := C.addInverseRight y
  have hsum :
      rAdd (rMulCandidate x y) (rMulCandidate x (rNeg y)) = rZero := by
    calc
      rAdd (rMulCandidate x y) (rMulCandidate x (rNeg y)) =
          rMulCandidate x (rAdd y (rNeg y)) := hd.symm
      _ = rMulCandidate x rZero := by rw [hy0]
      _ = rZero := mulZeroRight016 C x
  exact addInverseUnique016 C hsum

/-- Multiplication by an additive inverse on the left negates the product. -/
theorem mulNegLeft016
    (C : RWithoutOrderTotalCertificate)
    (x y : RBOMA) :
    rMulCandidate (rNeg x) y = rNeg (rMulCandidate x y) := by
  calc
    rMulCandidate (rNeg x) y = rMulCandidate y (rNeg x) :=
      C.mulComm (rNeg x) y
    _ = rNeg (rMulCandidate y x) := mulNegRight016 C y x
    _ = rNeg (rMulCandidate x y) := by rw [C.mulComm y x]

/-- Squaring a negated value gives the same square, using only accepted field laws. -/
theorem mulNegNegSame016
    (C : RWithoutOrderTotalCertificate)
    (x : RBOMA) :
    rMulCandidate (rNeg x) (rNeg x) = rMulCandidate x x := by
  calc
    rMulCandidate (rNeg x) (rNeg x) =
        rNeg (rMulCandidate x (rNeg x)) :=
      mulNegLeft016 C x (rNeg x)
    _ = rNeg (rNeg (rMulCandidate x x)) := by
      rw [mulNegRight016 C x x]
    _ = rMulCandidate x x := negInvolutive016 C _


theorem addLeftComm016
    (C : RWithoutOrderTotalCertificate) (a b c : RBOMA) :
    rAdd a (rAdd b c) = rAdd b (rAdd a c) := by
  calc
    rAdd a (rAdd b c) = rAdd (rAdd a b) c := (C.addAssoc a b c).symm
    _ = rAdd (rAdd b a) c := by rw [C.addComm a b]
    _ = rAdd b (rAdd a c) := C.addAssoc b a c

/-- Scalar multiplicative reassociation needed by the explicit normalizer. -/
theorem mulLeftComm016
    (C : RWithoutOrderTotalCertificate) (a b c : RBOMA) :
    rMulCandidate a (rMulCandidate b c) =
      rMulCandidate b (rMulCandidate a c) := by
  calc
    rMulCandidate a (rMulCandidate b c) =
        rMulCandidate (rMulCandidate a b) c := (C.mulAssoc a b c).symm
    _ = rMulCandidate (rMulCandidate b a) c := by rw [C.mulComm a b]
    _ = rMulCandidate b (rMulCandidate a c) := C.mulAssoc b a c

/-- Distribution in the first scalar argument is derived, not assumed. -/
theorem mulAddLeft016
    (C : RWithoutOrderTotalCertificate) (a b c : RBOMA) :
    rMulCandidate (rAdd a b) c =
      rAdd (rMulCandidate a c) (rMulCandidate b c) := by
  calc
    rMulCandidate (rAdd a b) c = rMulCandidate c (rAdd a b) :=
      C.mulComm (rAdd a b) c
    _ = rAdd (rMulCandidate c a) (rMulCandidate c b) :=
      C.distribRight c a b
    _ = rAdd (rMulCandidate a c) (rMulCandidate b c) := by
      rw [C.mulComm c a, C.mulComm c b]

/-- Additive inverse distributes over scalar addition using inverse uniqueness. -/
theorem negAdd016
    (C : RWithoutOrderTotalCertificate) (a b : RBOMA) :
    rNeg (rAdd a b) = rAdd (rNeg a) (rNeg b) := by
  have h : rAdd (rAdd a b) (rAdd (rNeg a) (rNeg b)) = rZero := by
    calc
      rAdd (rAdd a b) (rAdd (rNeg a) (rNeg b)) =
          rAdd a (rAdd b (rAdd (rNeg a) (rNeg b))) :=
        C.addAssoc a b (rAdd (rNeg a) (rNeg b))
      _ = rAdd a (rAdd (rNeg a) (rAdd b (rNeg b))) := by
        rw [addLeftComm016 C b (rNeg a) (rNeg b)]
      _ = rAdd (rAdd a (rNeg a)) (rAdd b (rNeg b)) :=
        (C.addAssoc a (rNeg a) (rAdd b (rNeg b))).symm
      _ = rZero := by
        rw [C.addInverseRight a, C.addInverseRight b, C.addZeroLeft rZero]
  exact (addInverseUnique016 C h).symm


theorem addCommPair016 (C : RWithoutOrderTotalCertificate) (z w : Pair004) :
    add004 z w = add004 w z := by
  apply pair_ext004
  · exact C.addComm z.re w.re
  · exact C.addComm z.im w.im

theorem addAssocPair016
    (C : RWithoutOrderTotalCertificate) (z w v : Pair004) :
    add004 (add004 z w) v = add004 z (add004 w v) := by
  apply pair_ext004
  · exact C.addAssoc z.re w.re v.re
  · exact C.addAssoc z.im w.im v.im

theorem addZeroLeftPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    add004 zero004 z = z := by
  apply pair_ext004
  · exact C.addZeroLeft z.re
  · exact C.addZeroLeft z.im

theorem addZeroRightPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    add004 z zero004 = z := by
  rw [addCommPair016 C z zero004, addZeroLeftPair016 C z]

theorem addNegRightPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    add004 z (neg004 z) = zero004 := by
  apply pair_ext004
  · exact C.addInverseRight z.re
  · exact C.addInverseRight z.im

theorem addNegLeftPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    add004 (neg004 z) z = zero004 := by
  rw [addCommPair016 C (neg004 z) z, addNegRightPair016 C z]

theorem negInvolutivePair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    neg004 (neg004 z) = z := by
  apply pair_ext004
  · exact negInvolutive016 C z.re
  · exact negInvolutive016 C z.im

theorem mulCommPair016 (C : RWithoutOrderTotalCertificate) (z w : Pair004) :
    mul004 z w = mul004 w z := by
  cases z <;> cases w <;>
    simp [mul004,
      mul004, C.mulComm, C.addComm]

/-- Associativity is an explicit consequence of the accepted real ring laws. -/
theorem mulAssocPair016
    (C : RWithoutOrderTotalCertificate) (z w v : Pair004) :
    mul004 (mul004 z w) v = mul004 z (mul004 w v) := by
  cases z <;> cases w <;> cases v <;>
    simp [mul004,
      mul004,
      mulAddLeft016 C, C.distribRight,
      mulNegLeft016 C, mulNegRight016 C,
      negAdd016 C, negInvolutive016 C,
      C.mulAssoc, C.mulComm, mulLeftComm016 C,
      C.addAssoc, C.addComm, addLeftComm016 C]

theorem mulOneLeftPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    mul004 one004 z = z := by
  apply pair_ext004
  · change
      rAdd (rMulCandidate rOne z.re)
        (rNeg (rMulCandidate rZero z.im)) = z.re
    rw [C.mulOneLeft z.re, mulZeroLeft016 C z.im,
      neg_zero004 C,
      add_zero_right004 C z.re]
  · change
      rAdd (rMulCandidate rOne z.im)
        (rMulCandidate rZero z.re) = z.im
    rw [C.mulOneLeft z.im, mulZeroLeft016 C z.re,
      add_zero_right004 C z.im]

theorem mulOneRightPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    mul004 z one004 = z := by
  rw [mulCommPair016 C z one004, mulOneLeftPair016 C z]

/-- Right distribution is proved independently from the abstract real interface. -/
theorem mulAddRightPair016
    (C : RWithoutOrderTotalCertificate) (z w v : Pair004) :
    mul004 z (add004 w v) = add004 (mul004 z w) (mul004 z v) := by
  cases z <;> cases w <;> cases v <;>
    simp [mul004, add004, mul004,
      add004, mul004,
      add004,
      mulAddLeft016 C, C.distribRight,
      mulNegLeft016 C, mulNegRight016 C,
      negAdd016 C, negInvolutive016 C,
      C.mulAssoc, C.mulComm, mulLeftComm016 C,
      C.addAssoc, C.addComm, addLeftComm016 C]

theorem mulAddLeftPair016
    (C : RWithoutOrderTotalCertificate) (z w v : Pair004) :
    mul004 (add004 z w) v = add004 (mul004 z v) (mul004 w v) := by
  calc
    mul004 (add004 z w) v = mul004 v (add004 z w) :=
      mulCommPair016 C (add004 z w) v
    _ = add004 (mul004 v z) (mul004 v w) := mulAddRightPair016 C v z w
    _ = add004 (mul004 z v) (mul004 w v) := by
      rw [mulCommPair016 C v z, mulCommPair016 C v w]

theorem mulZeroLeftPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    mul004 zero004 z = zero004 := by
  apply pair_ext004
  · change
      rAdd (rMulCandidate rZero z.re)
        (rNeg (rMulCandidate rZero z.im)) = rZero
    rw [mulZeroLeft016 C z.re,
      mulZeroLeft016 C z.im,
      neg_zero004 C, C.addZeroLeft rZero]
  · change
      rAdd (rMulCandidate rZero z.im)
        (rMulCandidate rZero z.re) = rZero
    rw [mulZeroLeft016 C z.im,
      mulZeroLeft016 C z.re, C.addZeroLeft rZero]

theorem mulZeroRightPair016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    mul004 z zero004 = zero004 := by
  rw [mulCommPair016 C z zero004, mulZeroLeftPair016 C z]



/-- Research-only Route-P conjugation and unchanged quadratic norm. -/
def conj016 (z : Pair004) : Pair004 := ⟨z.re, rNeg z.im⟩

theorem mulConj016 (C : RWithoutOrderTotalCertificate) (z : Pair004) :
    mul004 z (conj016 z) = ofR004 (norm016 z) := by
  apply pair_ext004
  · change
      rAdd (rMulCandidate z.re z.re)
        (rNeg (rMulCandidate z.im (rNeg z.im))) =
      rAdd (rMulCandidate z.re z.re) (rMulCandidate z.im z.im)
    rw [mulNegRight016 C z.im z.im,
      negInvolutive016 C (rMulCandidate z.im z.im)]
  · change
      rAdd (rMulCandidate z.re (rNeg z.im))
        (rMulCandidate z.im z.re) = rZero
    rw [mulNegRight016 C z.re z.im,
      C.mulComm z.im z.re,
      C.addComm (rNeg (rMulCandidate z.re z.im))
        (rMulCandidate z.re z.im),
      C.addInverseRight (rMulCandidate z.re z.im)]

theorem inverseFromScalar016
    (C : RWithoutOrderTotalCertificate) (z : Pair004) (t : RBOMA)
    (ht : rMulCandidate (norm016 z) t = rOne) :
    mul004 z (mul004 (ofR004 t) (conj016 z)) = one004 := by
  calc
    mul004 z (mul004 (ofR004 t) (conj016 z)) =
        mul004 z (mul004 (conj016 z) (ofR004 t)) := by
      rw [mulCommPair016 C (ofR004 t) (conj016 z)]
    _ = mul004 (mul004 z (conj016 z)) (ofR004 t) :=
      (mulAssocPair016 C z (conj016 z) (ofR004 t)).symm
    _ = mul004 (ofR004 (norm016 z)) (ofR004 t) := by
      rw [mulConj016 C z]
    _ = ofR004 (rMulCandidate (norm016 z) t) :=
      (ofR_mul004 C (norm016 z) t).symm
    _ = ofR004 rOne := by rw [ht]
    _ = one004 := ofR_one004

theorem complexInverseExists016 (C : RNormAnisotropyCertificate016)
    (z : Pair004) (hz : z ≠ zero004) :
    ∃ w : Pair004, mul004 z w = one004 := by
  rcases normScalarInverseExists016 C hz with ⟨t, ht⟩
  exact ⟨mul004 (ofR004 t) (conj016 z),
    inverseFromScalar016 C.scalar z t ht⟩

theorem complexInverseUnique016
    (C : RWithoutOrderTotalCertificate)
    {z w v : Pair004}
    (hw : mul004 z w = one004)
    (hv : mul004 z v = one004) : w = v := by
  calc
    w = mul004 w one004 := (mulOneRightPair016 C w).symm
    _ = mul004 w (mul004 z v) := by rw [hv]
    _ = mul004 (mul004 w z) v :=
      (mulAssocPair016 C w z v).symm
    _ = mul004 one004 v := by rw [mulCommPair016 C w z, hw]
    _ = v := mulOneLeftPair016 C v

/-- The complete witness-field *research package*, without the obsolete
    auxiliary normNonnegative property. This is not an accepted producer. -/
structure FieldCertificate016 (C : RNormAnisotropyCertificate016) : Prop where
  addComm : ∀ z w : Pair004, add004 z w = add004 w z
  addAssoc : ∀ z w v : Pair004, add004 (add004 z w) v = add004 z (add004 w v)
  addZero : ∀ z : Pair004, add004 zero004 z = z
  addInverse : ∀ z : Pair004, add004 z (neg004 z) = zero004
  mulComm : ∀ z w : Pair004, mul004 z w = mul004 w z
  mulAssoc : ∀ z w v : Pair004, mul004 (mul004 z w) v = mul004 z (mul004 w v)
  mulOne : ∀ z : Pair004, mul004 one004 z = z
  distrib : ∀ z w v : Pair004, mul004 z (add004 w v) =
    add004 (mul004 z w) (mul004 z v)
  normNonzero : ∀ z : Pair004, z ≠ zero004 → norm016 z ≠ rZero
  conjProduct : ∀ z : Pair004, mul004 z (conj016 z) = ofR004 (norm016 z)
  inverseExists : ∀ z : Pair004, z ≠ zero004 → ∃ w : Pair004, mul004 z w = one004
  inverseUnique : ∀ {z w v : Pair004},
    mul004 z w = one004 → mul004 z v = one004 → w = v

theorem fieldCertificate016 (C : RNormAnisotropyCertificate016) :
    FieldCertificate016 C where
  addComm := addCommPair016 C.scalar
  addAssoc := addAssocPair016 C.scalar
  addZero := addZeroLeftPair016 C.scalar
  addInverse := addNegRightPair016 C.scalar
  mulComm := mulCommPair016 C.scalar
  mulAssoc := mulAssocPair016 C.scalar
  mulOne := mulOneLeftPair016 C.scalar
  distrib := mulAddRightPair016 C.scalar
  normNonzero := fun _ hz => normNonzero016 C hz
  conjProduct := mulConj016 C.scalar
  inverseExists := complexInverseExists016 C
  inverseUnique := @complexInverseUnique016 C.scalar

/-- Research integration candidate: exact Gate-E seven-family certificate
plus the algebraically rebuilt field and explicit 011 coordinate comparison.
Claim-surface correspondence still requires Gate D semantic audit. -/
structure NineClaimCandidate016 (C : RNormAnisotropyCertificate016) where
  controls : CSurvivorCertificate004 C.scalar
  field : FieldCertificate016 C
  comparison : ∀ (B : BOMA.C.StageTwo.ComparisonInterface011.QuadraticPresentation
      scalarOps004),
    BOMA.C.StageTwo.ComparisonInterface011.QuadraticComparisonCertificate
      comparisonPresentation004 B
  functionalComparison : ∀
    (B : BOMA.C.StageTwo.ComparisonInterface011.QuadraticPresentation scalarOps004),
    BOMA.C.StageTwo.ComparisonInterface011.CoordinateExtractor B →
    BOMA.C.StageTwo.ComparisonInterface011.ConstructiveQuadraticIsomorphism
      comparisonPresentation004 B

/-- No choice: the local pair exposes both coordinates by projection. -/
def explicitPairExtractor016 :
    BOMA.C.StageTwo.ComparisonInterface011.CoordinateExtractor
      comparisonPresentation004 where
  re := fun z => z.re
  im := fun z => z.im
  sound := fun _ => rfl

theorem anyQuadraticComparison016
    (B : BOMA.C.StageTwo.ComparisonInterface011.QuadraticPresentation scalarOps004) :
    BOMA.C.StageTwo.ComparisonInterface011.QuadraticComparisonCertificate
      comparisonPresentation004 B :=
  BOMA.C.StageTwo.ComparisonInterface011.quadraticComparison
    comparisonPresentation004 B

def explicitFunctionalComparison016
    (B : BOMA.C.StageTwo.ComparisonInterface011.QuadraticPresentation scalarOps004)
    (EB : BOMA.C.StageTwo.ComparisonInterface011.CoordinateExtractor B) :
    BOMA.C.StageTwo.ComparisonInterface011.ConstructiveQuadraticIsomorphism
      comparisonPresentation004 B :=
  BOMA.C.StageTwo.ComparisonInterface011.constructiveQuadraticIsomorphism
    comparisonPresentation004 B explicitPairExtractor016 EB

def nineClaimCandidate016 (C : RNormAnisotropyCertificate016) :
    NineClaimCandidate016 C where
  controls := cSurvivorCertificate004 C.scalar
  field := fieldCertificate016 C
  comparison := anyQuadraticComparison016
  functionalComparison := explicitFunctionalComparison016

end BOMA.C.StageTwo.NormAnisotropy016
